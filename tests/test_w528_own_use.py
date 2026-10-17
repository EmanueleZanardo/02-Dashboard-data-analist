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
    assert len(titoli) == 531
    assert TITLE528 in titoli
    assert TITLE527 in titoli
    assert src.count(TITLE528) == 3
    assert ", tab527, tab528, tab529, tab530, tab531 = st.tabs([" in src
    # chiavi widget st528_* univoche (13 pattern attesi)
    keys = re.findall(r'key=f?"(st528_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 11
