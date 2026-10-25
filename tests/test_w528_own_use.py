"""Test tab528 '⚖️🔌 Own-use exemption NPNS (IFRS 9 2.4)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh528_num", "mh528_str", "mh528_bool", "mh528_voce",
           "mh528_misura", "mh528_riepilogo")

TITLE528 = "⚖️🔌 Own-use exemption NPNS (IFRS 9 2.4)"
TITLE527 = "⚖️📉 Ammortamento adeguamento FV hedge (IFRS 9 6.5.10)"


def _c(cid="C-1", tipo="acquisto", netto=True, prassi=False, fisica=True,
       fab=50000.0, qta=40000.0, des=False, d="x"):
    return {"id": cid, "tipo": tipo, "regolamento_netto_possibile": netto,
            "prassi_net_settlement_trading": prassi,
            "consegna_fisica_prevista": fisica,
            "fabbisogno_atteso_mwh": fab, "qta_contratto_mwh": qta,
            "designa_fvtpl_mismatch": des, "descrizione": d}


class TestW528Validatori:
    def test_num_ok(self):
        assert _F["mh528_num"](2, "x") == 2.0
        assert _F["mh528_num"](-1.5, "x") == -1.5
        assert _F["mh528_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh528_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh528_str"]("  C-1 ", "x") == "C-1"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh528_str"](bad, "x")

    def test_bool_ok(self):
        assert _F["mh528_bool"](True, "x") is True
        assert _F["mh528_bool"](False, "x") is False

    def test_bool_ko(self):
        for bad in (1, 0, "si", None):
            with pytest.raises(ValueError):
                _F["mh528_bool"](bad, "x")


class TestW528Voce:
    def test_ok_normalizza(self):
        r = _F["mh528_voce"](_c())
        assert r["id"] == "C-1"
        assert r["qta_contratto_mwh"] == 40000.0
        assert r["descrizione"] == "x"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh528_voce"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh528_voce"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(cid="  "))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(qta=0.0))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(qta=-5.0))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(fab=0.0))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(tipo="swap"))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(netto=1))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(prassi="no"))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(qta=math.nan))
        with pytest.raises(ValueError):
            _F["mh528_voce"](_c(fab=math.inf))
        v = _c()
        v["descrizione"] = 7
        with pytest.raises(ValueError):
            _F["mh528_voce"](v)


class TestW528Misura:
    def test_own_use_esente(self):
        r = _F["mh528_misura"](_c())
        assert r["esito"] == "OWN_USE_ESENTE"
        assert r["mwh_esenti"] == 40000.0
        assert r["mwh_fvtpl"] == 0.0

    def test_own_use_boundary_qta_uguale_fabbisogno(self):
        r = _F["mh528_misura"](_c(qta=50000.0, fab=50000.0))
        assert r["esito"] == "OWN_USE_ESENTE"

    def test_non_derivato(self):
        r = _F["mh528_misura"](_c(netto=False))
        assert r["esito"] == "NON_DERIVATO"
        assert r["mwh_esenti"] == 0.0 and r["mwh_fvtpl"] == 0.0

    def test_opzione_emessa_sempre_fvtpl(self):
        r = _F["mh528_misura"](_c(tipo="opzione_emessa"))
        assert r["esito"] == "IN_SCOPE_FVTPL"
        assert r["mwh_fvtpl"] == 40000.0

    def test_prassi_trading_taint(self):
        r = _F["mh528_misura"](_c(prassi=True))
        assert r["esito"] == "IN_SCOPE_FVTPL"

    def test_qta_eccedente(self):
        r = _F["mh528_misura"](_c(qta=60000.0))
        assert r["esito"] == "IN_SCOPE_FVTPL"

    def test_consegna_fisica_non_prevista(self):
        r = _F["mh528_misura"](_c(fisica=False))
        assert r["esito"] == "IN_SCOPE_FVTPL"

    def test_designato_fvtpl(self):
        r = _F["mh528_misura"](_c(des=True))
        assert r["esito"] == "DESIGNATO_FVTPL"
        assert r["mwh_fvtpl"] == 40000.0
        assert r["mwh_esenti"] == 0.0


class TestW528Riepilogo:
    def test_tutti_esenti(self):
        r = _F["mh528_riepilogo"]([_c("A"), _c("B")])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_ESENTI"
        assert t["n_esenti"] == 2
        assert t["mwh_esenti"] == 80000.0
        assert t["mwh_fvtpl"] == 0.0

    def test_tutti_fvtpl(self):
        r = _F["mh528_riepilogo"]([_c("A", prassi=True),
                                   _c("B", tipo="opzione_emessa")])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_FVTPL"
        assert t["n_fvtpl"] == 2
        assert t["mwh_fvtpl"] == 80000.0

    def test_nessun_derivato(self):
        r = _F["mh528_riepilogo"]([_c("A", netto=False)])
        assert r["totali"]["verdetto_complessivo"] == "NESSUN_DERIVATO"

    def test_misto(self):
        r = _F["mh528_riepilogo"]([_c("A"), _c("B", prassi=True),
                                   _c("C", netto=False)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "MISTO"
        assert (t["n_esenti"], t["n_fvtpl"], t["n_non_derivato"]) == (1, 1, 1)
        assert t["mwh_esenti"] == 40000.0
        assert t["mwh_fvtpl"] == 40000.0

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh528_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh528_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh528_riepilogo"]([_c("A"), _c("A")])


def test_registry_tab528():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 699
    assert TITLE528 in titoli
    assert TITLE527 in titoli
    assert src.count(TITLE528) == 3
    assert ", tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699 = st.tabs([" in src
    # chiavi widget st528_* univoche (13 pattern attesi)
    keys = re.findall(r'key=f?"(st528_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 11
