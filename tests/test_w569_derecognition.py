"""Test tab569 "Utili/perdite da derecognition di attivita' al costo
ammortizzato (IFRS 7.20A)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh569_num", "mh569_str", "mh569_categoria", "mh569_motivo",
           "mh569_evento", "mh569_demo", "mh569_riepilogo")

TITLE569 = ("\U0001F4CA\U0001F4C9 Utili/perdite da derecognition di "
            "attivit\xe0 al costo ammortizzato (IFRS 7.20A)")


def _v(pid="DRC-1", descrizione="pos", cat="CREDITI_COMMERCIALI",
       mot="VENDITA_ATTIVA", data="2026-01-31", vc=10_000_000.0,
       co=10_400_000.0):
    return _F["mh569_evento"](pid, descrizione, cat, mot, data, vc, co)


class TestW569Validatori:
    def test_num_ok(self):
        assert _F["mh569_num"](2, "x") == 2.0
        assert _F["mh569_num"](-3.5, "x") == -3.5
        assert _F["mh569_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh569_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh569_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh569_str"](bad, "x")

    def test_categoria_ok(self):
        assert _F["mh569_categoria"]("crediti_ppa", "x") == "CREDITI_PPA"
        assert _F["mh569_categoria"]("TITOLI_DEBITO", "x") == "TITOLI_DEBITO"
        assert _F["mh569_categoria"]("finanziamenti",
                                     "x") == "FINANZIAMENTI"

    def test_categoria_ko(self):
        for bad in ("XYZ", "", None, "DERIVATI"):
            with pytest.raises(ValueError):
                _F["mh569_categoria"](bad, "x")

    def test_motivo_ok(self):
        assert _F["mh569_motivo"]("vendita_attiva",
                                  "x") == "VENDITA_ATTIVA"
        assert _F["mh569_motivo"]("CARTOLARIZZAZIONE",
                                  "x") == "CARTOLARIZZAZIONE"
        assert _F["mh569_motivo"]("altro", "x") == "ALTRO"

    def test_motivo_ko(self):
        for bad in ("FURTO", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh569_motivo"](bad, "x")


class TestW569Evento:
    def test_hand_computed(self):
        r = _v(pid="DRC-001", vc=12_000_000.0, co=12_600_000.0)
        assert r["id"] == "DRC-001"
        assert r["categoria"] == "CREDITI_COMMERCIALI"
        assert r["motivo"] == "VENDITA_ATTIVA"
        assert r["valore_contabile"] == pytest.approx(12_000_000.0)
        assert r["corrispettivo"] == pytest.approx(12_600_000.0)
        assert r["pnl"] == pytest.approx(600_000.0)
        assert r["segno"] == "UTILE"

    def test_segno_perdita(self):
        r = _v(vc=8_000_000.0, co=7_700_000.0)
        assert r["pnl"] == pytest.approx(-300_000.0)
        assert r["segno"] == "PERDITA"

    def test_segno_neutro(self):
        r = _v(vc=5_000_000.0, co=5_000_000.0)
        assert r["pnl"] == pytest.approx(0.0)
        assert r["segno"] == "NEUTRO"

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(cat="XYZ")
        with pytest.raises(ValueError):
            _v(mot="REGALO")
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(vc=math.nan)
        with pytest.raises(ValueError):
            _v(data="   ")


class TestW569Demo:
    def test_demo_shape(self):
        d = _F["mh569_demo"]()
        assert len(d) == 3
        assert all(set(r) >= {"valore_contabile", "corrispettivo", "pnl",
                              "segno", "motivo"} for r in d)

    def test_demo_verdetto(self):
        r = _F["mh569_riepilogo"](_F["mh569_demo"]())
        assert r["verdetto"] == "IMPATTO_CONTENUTO"
        assert r["n_anomalie"] == 0
        assert r["pnl_netto"] == pytest.approx(350_000.0)
        # +600k - 300k + 50k
        assert r["utili_totali"] == pytest.approx(650_000.0)
        assert r["perdite_totali"] == pytest.approx(-300_000.0)

    def test_demo_vc_totale(self):
        r = _F["mh569_riepilogo"](_F["mh569_demo"]())
        assert r["valore_contabile_totale"] == pytest.approx(25_000_000.0)


class TestW569Riepilogo:
    def test_utile_significativo_soglia_bassa(self):
        rs = [_v(pid="A", vc=10_000_000.0, co=12_000_000.0)]
        r = _F["mh569_riepilogo"](rs, soglia_eur=1_000_000.0)
        assert r["verdetto"] == "UTILE_NETTO_SIGNIFICATIVO"
        assert r["n_anomalie"] == 0

    def test_perdita_significativa(self):
        rs = [_v(pid="A", vc=10_000_000.0, co=8_000_000.0)]
        r = _F["mh569_riepilogo"](rs, soglia_eur=1_000_000.0)
        assert r["verdetto"] == "PERDITA_NETTA_SIGNIFICATIVA"
        assert r["perdite_totali"] == pytest.approx(-2_000_000.0)

    def test_impatto_contenuto(self):
        rs = [_v(pid="A", vc=10_000_000.0, co=10_400_000.0)]
        r = _F["mh569_riepilogo"](rs, soglia_eur=1_000_000.0)
        assert r["verdetto"] == "IMPATTO_CONTENUTO"

    def test_nessuna_derecognition(self):
        r = _F["mh569_riepilogo"]([_v(vc=0.0, co=0.0)])
        assert r["verdetto"] == "NESSUNA_DERECOGNITION"

    def test_anomalia_vc_non_positivo(self):
        # convenzione tab566/567/568: NESSUNA_DERECOGNITION prevale sul
        # solo evento anomalo, quindi serve un evento valido accanto
        r = _F["mh569_riepilogo"]([_v(pid="A"), _v(pid="B", vc=-1.0,
                                            co=5.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("valore contabile" in a.lower()
                   for p in r["analizzati"] for a in p["anomalie"])

    def test_anomalia_corrispettivo_negativo(self):
        r = _F["mh569_riepilogo"]([_v(vc=10.0, co=-5.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("corrispettivo negativo" in a.lower()
                   for p in r["analizzati"] for a in p["anomalie"])

    def test_anomalia_sproporzione(self):
        # perdita del 50% del VC: oltre il 30%
        r = _F["mh569_riepilogo"]([_v(vc=10_000_000.0, co=5_000_000.0)])
        assert any("30%" in a for p in r["analizzati"]
                   for a in p["anomalie"])

    def test_sproporzione_sotto_soglia_ok(self):
        # 10% di scarto: nessuna anomalia di proporzionalita'
        r = _F["mh569_riepilogo"]([_v(vc=10_000_000.0, co=9_000_000.0)])
        assert r["n_anomalie"] == 0

    def test_anomalia_id_duplicato(self):
        r = _F["mh569_riepilogo"]([_v(pid="DRC-X"), _v(pid="drc-x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_anomalie_prevalgono_su_significativo(self):
        rs = [_v(pid="DRC-X", vc=10_000_000.0, co=20_000_000.0),
              _v(pid="DRC-X", vc=10_000_000.0, co=10_000_000.0)]
        r = _F["mh569_riepilogo"](rs, soglia_eur=1_000_000.0)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_utili_perdite_separati(self):
        rs = [_v(pid="A", vc=10_000_000.0, co=11_000_000.0),
              _v(pid="B", vc=10_000_000.0, co=9_500_000.0)]
        r = _F["mh569_riepilogo"](rs, soglia_eur=1_000_000.0)
        assert r["utili_totali"] == pytest.approx(1_000_000.0)
        assert r["perdite_totali"] == pytest.approx(-500_000.0)
        assert r["pnl_netto"] == pytest.approx(500_000.0)
        assert r["verdetto"] == "IMPATTO_CONTENUTO"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh569_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (0.0, -100.0):
            with pytest.raises(ValueError):
                _F["mh569_riepilogo"](_F["mh569_demo"](),
                                      soglia_eur=bad)


class TestW569Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE569}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 590
        assert TITLE569 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590 = st.tabs([" in src
        assert "with tab569:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st569_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
