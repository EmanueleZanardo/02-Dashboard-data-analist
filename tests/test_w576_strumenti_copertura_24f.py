"""Test tab576 "Strumenti di copertura per categoria di rischio (IFRS 7.24F)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh576_num", "mh576_str", "mh576_rischio", "mh576_tipo",
           "mh576_unita", "mh576_strumento", "mh576_demo",
           "mh576_riepilogo")

TITLE576 = "📊🗂️ Strumenti di copertura per categoria di rischio (IFRS 7.24F)"


def _s(sid="HDG-1", descrizione="strumento", rischio="COMMODITY",
       tipo="CASH_FLOW", att=500_000.0, pas=100_000.0,
       voce="Derivati di copertura - attivita", fv=-120_000.0,
       not_=2_000.0, un="T"):
    return _F["mh576_strumento"](sid, descrizione, rischio, tipo, att,
                                 pas, voce, fv,
                                 nozionale_importo=not_,
                                 nozionale_unita=un)


class TestW576Validatori:
    def test_num_ok(self):
        assert _F["mh576_num"](2, "x") == 2.0
        assert _F["mh576_num"](-3.5, "x") == -3.5
        assert _F["mh576_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh576_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh576_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh576_str"](bad, "x")

    def test_rischio_ok(self):
        assert _F["mh576_rischio"]("tasso") == "TASSO"
        assert _F["mh576_rischio"]("Commodity") == "COMMODITY"
        assert _F["mh576_rischio"]("FX") == "FX"
        assert _F["mh576_rischio"]("credito") == "CREDITO"
        assert _F["mh576_rischio"]("altro") == "ALTRO"

    def test_rischio_ko(self):
        for bad in ("MKT", "", None, "tassi"):
            with pytest.raises(ValueError):
                _F["mh576_rischio"](bad)

    def test_tipo_unita_ok(self):
        assert _F["mh576_tipo"]("cash flow") == "CASH_FLOW"
        assert _F["mh576_tipo"]("NET_INVESTMENT") == "NET_INVESTMENT"
        assert _F["mh576_unita"]("eur") == "EUR"
        assert _F["mh576_unita"]("M3") == "M3"
        assert _F["mh576_unita"]("mwh") == "MWH"

    def test_tipo_ko(self):
        for bad in ("FV", "", None, "cashflow"):
            with pytest.raises(ValueError):
                _F["mh576_tipo"](bad)

    def test_unita_ko(self):
        for bad in ("JPY", "", None, "ton"):
            with pytest.raises(ValueError):
                _F["mh576_unita"](bad)


class TestW576Strumento:
    def test_hand_computed(self):
        r = _s()
        assert r["valore_att"] == pytest.approx(500_000.0)
        assert r["valore_pass"] == pytest.approx(100_000.0)
        assert r["variazione_fv"] == pytest.approx(-120_000.0)
        assert r["nozionale_importo"] == pytest.approx(2_000.0)
        assert r["nozionale_unita"] == "T"
        assert r["fisico"] is True
        assert r["rischio_label"] == "Commodity"
        assert r["tipo_label"] == "Cash flow hedges"
        assert r["completa"] and r["anomalie"] == []

    def test_voce_vuota_anomalia(self):
        r = _s(voce="   ")
        assert not r["completa"]
        assert any("Voce di stato patrimoniale non indicata" in a
                   for a in r["anomalie"])

    def test_nozionale_zero_anomalia(self):
        r = _s(not_=0.0)
        assert not r["completa"]
        assert any("Nozionale nullo o negativo" in a
                   for a in r["anomalie"])

    def test_nozionale_negativo_anomalia(self):
        r = _s(not_=-5.0)
        assert any("Nozionale nullo o negativo" in a
                   for a in r["anomalie"])

    def test_nozionale_none_anomalia(self):
        r = _F["mh576_strumento"]("HDG-1", "s", "FX", "CASH_FLOW",
                                  10.0, 0.0, "voce", 0.0,
                                  nozionale_importo=None)
        assert any("Nozionale non dichiarato" in a
                   for a in r["anomalie"])

    def test_fv_none_anomalia(self):
        r = _s(fv=None)
        assert r["variazione_fv"] == 0.0
        assert any("Variazione fair value non dichiarata" in a
                   for a in r["anomalie"])

    def test_fv_non_numerico_ko(self):
        with pytest.raises(ValueError):
            _s(fv="x")

    def test_valori_contabili_zero_anomalia(self):
        r = _s(att=0.0, pas=0.0)
        assert any("Nessun valore contabile rilevato" in a
                   for a in r["anomalie"])

    def test_fisico_flag(self):
        assert _s(un="EUR")["fisico"] is False
        assert _s(un="M3")["fisico"] is True
        assert _s(un="MWH")["fisico"] is True

    def test_strip(self):
        r = _s(sid="  HDG-X  ", descrizione="  d  ", rischio="fx",
               voce="  voce x  ")
        assert r["id"] == "HDG-X"
        assert r["rischio"] == "FX"
        assert r["voce_bilancio"] == "voce x"


class TestW576Riepilogo:
    def test_demo_disclosure_completa(self):
        r = _F["mh576_riepilogo"](_F["mh576_demo"]())
        # att = 450k + 1.2M; pass = 300k + 180k; netto = 1.17M
        assert r["totale_att"] == pytest.approx(1_650_000.0)
        assert r["totale_pass"] == pytest.approx(480_000.0)
        assert r["valore_netto"] == pytest.approx(1_170_000.0)
        assert r["n_strumenti"] == 3
        assert r["n_anomalie"] == 0
        assert r["n_nozionali_fisici"] == 1
        assert r["verdetto"] == "DISCLOSURE_COMPLETA"
        vt = r["valore_per_tipo"]
        assert vt["Fair value hedges"] == {"att": pytest.approx(
            450_000.0), "pass": pytest.approx(0.0)}
        assert vt["Cash flow hedges"] == {"att": pytest.approx(
            1_200_000.0), "pass": pytest.approx(300_000.0)}
        assert vt["Net investment hedges"] == {"att": pytest.approx(
            0.0), "pass": pytest.approx(180_000.0)}
        npr = r["nozionale_per_rischio"]
        assert npr["Tasso di interesse"] == {"EUR": pytest.approx(
            10_000_000.0)}
        assert npr["Commodity"] == {"T": pytest.approx(25_000.0)}
        assert npr["Cambio"] == {"EUR": pytest.approx(5_000_000.0)}

    def test_nessuno_strumento(self):
        r = _F["mh576_riepilogo"]([])
        assert r["verdetto"] == "NESSUNO_STRUMENTO"
        assert r["n_strumenti"] == 0
        assert r["valore_per_tipo"]["Fair value hedges"]["att"] == 0.0

    def test_duplicati_anomalia(self):
        r = _F["mh576_riepilogo"]([_s(sid="DUP"), _s(sid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"]
                   for x in r["analizzati"])

    def test_anomalie_hanno_priorita(self):
        bad = _s(voce="")
        r = _F["mh576_riepilogo"]([bad])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_nozionale_e_valori_per_rischio_tipo(self):
        r = _F["mh576_riepilogo"]([_s(sid="A", rischio="TASSO",
                                      tipo="FAIR_VALUE", att=100.0,
                                      pas=0.0, not_=1_000.0, un="EUR"),
                                   _s(sid="B", rischio="TASSO",
                                      tipo="FAIR_VALUE", att=0.0,
                                      pas=50.0, not_=500.0, un="EUR")])
        assert r["nozionale_per_rischio"]["Tasso di interesse"] == \
            {"EUR": pytest.approx(1_500.0)}
        assert r["valore_per_tipo"]["Fair value hedges"] == \
            {"att": pytest.approx(100.0), "pass": pytest.approx(50.0)}


class TestW576Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE576}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 713
        assert TITLE576 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713 = st.tabs([" in src
        assert "with tab576:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st576_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
