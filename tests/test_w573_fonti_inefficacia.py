"""Test tab573 "Fonti di inefficacia delle coperture (IFRS 7.24D)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh573_num", "mh573_str", "mh573_relazione", "mh573_demo",
           "mh573_riepilogo")

TITLE573 = "📊⚠️ Fonti di inefficacia delle coperture (IFRS 7.24D)"


def _r(rid="COP-1", descrizione="relazione", tot=-450_000.0,
       tmp=120_000.0, base=180_000.0, cred=90_000.0, costo=40_000.0,
       altro=20_000.0):
    return _F["mh573_relazione"](rid, descrizione, tot, tmp, base, cred,
                                 costo, altro)


class TestW573Validatori:
    def test_num_ok(self):
        assert _F["mh573_num"](2, "x") == 2.0
        assert _F["mh573_num"](-3.5, "x") == -3.5
        assert _F["mh573_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh573_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh573_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh573_str"](bad, "x")


class TestW573Relazione:
    def test_hand_computed(self):
        r = _r()
        assert r["id"] == "COP-1"
        assert r["somma_quote"] == pytest.approx(450_000.0)
        assert r["completa"] is True
        assert r["anomalie"] == []

    def test_segnatura_positiva(self):
        r = _r(tot=1_200_000.0, tmp=500_000.0, base=400_000.0,
               cred=200_000.0, costo=100_000.0, altro=0.0)
        assert r["somma_quote"] == pytest.approx(1_200_000.0)
        assert r["completa"] is True

    def test_quota_negativa_anomalia(self):
        r = _r(tmp=-5.0)
        assert r["completa"] is False
        assert any("Disallineamento temporale" in a for a in r["anomalie"])

    def test_somma_non_quadra_anomalia(self):
        r = _r(tot=-450_000.0, tmp=100_000.0, base=180_000.0,
               cred=90_000.0, costo=40_000.0, altro=20_000.0)
        assert r["completa"] is False
        assert any("somma quote" in a for a in r["anomalie"])

    def test_somma_tolleranza_ok(self):
        # scarto 0.005 EUR entro la tolleranza 0.01 -> nessuna anomalia
        r = _r(tot=-450_000.005)
        assert r["completa"] is True

    def test_inefficacia_senza_fonti_anomalia(self):
        r = _r(tot=-100_000.0, tmp=0.0, base=0.0, cred=0.0, costo=0.0,
               altro=0.0)
        assert any("fonti allocate" in a for a in r["anomalie"])

    def test_quote_con_totale_nullo_anomalia(self):
        r = _r(tot=0.0)
        assert any("inefficacia totale nulla" in a for a in r["anomalie"])

    def test_totale_zero_quote_zero_ok(self):
        r = _r(tot=0.0, tmp=0.0, base=0.0, cred=0.0, costo=0.0, altro=0.0)
        assert r["completa"] is True

    def test_str_strip(self):
        r = _r(rid="  COP-X ", descrizione=" rel ")
        assert r["id"] == "COP-X"
        assert r["descrizione"] == "rel"


class TestW573Riepilogo:
    def test_demo_inefficacia_significativa(self):
        r = _F["mh573_riepilogo"](_F["mh573_demo"]())
        # |tot| = 450k + 1200k + 80k = 1.73M > 1M
        assert r["inefficacia_assoluta_totale"] == pytest.approx(1_730_000.0)
        assert r["n_relazioni"] == 3
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "INEFFICACIA_SIGNIFICATIVA"
        assert r["fonte_principale"] == "Disallineamento temporale"
        assert r["importo_fonte_principale"] == pytest.approx(650_000.0)
        assert r["totale_per_fonte"]["Rischio di base"] == pytest.approx(600_000.0)
        assert r["totale_per_fonte"]["Rischio di credito controparte"] == \
            pytest.approx(305_000.0)

    def test_inefficacia_gestibile(self):
        r = _F["mh573_riepilogo"]([_r()], soglia_eur=1_000_000.0)
        assert r["verdetto"] == "INEFFICACIA_GESTIBILE"

    def test_nessuna_relazione(self):
        r = _F["mh573_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_RELAZIONE"
        assert r["n_relazioni"] == 0

    def test_duplicati_anomalia(self):
        r = _F["mh573_riepilogo"]([_r(rid="DUP"), _r(rid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"] for x in r["analizzate"])

    def test_anomalie_hanno_priorita(self):
        # sopra soglia MA con anomalia -> ANOMALIE_DA_VERIFICARE
        r = _F["mh573_riepilogo"]([_r(tot=-2_000_000.0, tmp=100_000.0,
                                      base=180_000.0, cred=90_000.0,
                                      costo=40_000.0, altro=20_000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"


class TestW573Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE573}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 713
        assert TITLE573 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713 = st.tabs([" in src
        assert "with tab573:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st573_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
