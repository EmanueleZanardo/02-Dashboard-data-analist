"""Test tab530 '🔗📄 Derivati incorporati (IFRS 9 4.3)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh530_num", "mh530_str", "mh530_bool", "mh530_voce",
           "mh530_misura", "mh530_riepilogo")

TITLE530 = "🔗📄 Derivati incorporati (IFRS 9 4.3)"
TITLE529 = "⚖️⏹️ Cessazione hedge accounting (IFRS 9 6.5.12)"


def _c(cid="C-1", tipo="indicizzazione_prezzo", host="gas", rif="Brent",
       corr=False, auto=True, fv=False, fvi=45000.0, d="x"):
    return {"id": cid, "tipo_derivato": tipo, "commodity_host": host,
            "riferimento": rif, "strettamente_correlato": corr,
            "componente_derivato_autonomo": auto, "ibrido_al_fvtpl": fv,
            "fv_iniziale_eur": fvi, "descrizione": d}


class TestW530Validatori:
    def test_num_ok(self):
        assert _F["mh530_num"](2, "x") == 2.0
        assert _F["mh530_num"](-1.5, "x") == -1.5
        assert _F["mh530_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh530_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh530_str"]("  C-1 ", "x") == "C-1"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh530_str"](bad, "x")

    def test_bool_ok(self):
        assert _F["mh530_bool"](True, "x") is True
        assert _F["mh530_bool"](False, "x") is False

    def test_bool_ko(self):
        for bad in (1, 0, "sì", None):
            with pytest.raises(ValueError):
                _F["mh530_bool"](bad, "x")


class TestW530Voce:
    def test_ok_normalizza(self):
        v = _F["mh530_voce"](_c())
        assert v["id"] == "C-1"
        assert v["tipo_derivato"] == "indicizzazione_prezzo"
        assert v["commodity_host"] == "gas"
        assert v["riferimento"] == "Brent"
        assert v["strettamente_correlato"] is False
        assert v["fv_iniziale_eur"] == 45000.0
        assert v["descrizione"] == "x"

    def test_descrizione_default(self):
        v = dict(_c())
        del v["descrizione"]
        assert _F["mh530_voce"](v)["descrizione"] == ""

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh530_voce"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh530_voce"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(cid="  "))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(tipo="swap"))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(host=""))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(rif="  "))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(corr=1))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(auto="sì"))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(fv=None))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(fvi=True))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(fvi=math.nan))
        with pytest.raises(ValueError):
            _F["mh530_voce"](_c(fvi=math.inf))
        v = _c()
        v["descrizione"] = 7
        with pytest.raises(ValueError):
            _F["mh530_voce"](v)


class TestW530Misura:
    def test_scorpora_indicizzazione_non_correlata(self):
        # gas indicizzato al Brent: non correlato -> SCORPORA
        r = _F["mh530_misura"](_c())
        assert r["esito"] == "SCORPORA"
        assert r["fv_separato_eur"] == 45000.0

    def test_scorpora_fv_negativo(self):
        r = _F["mh530_misura"](_c(fvi=-12000.0))
        assert r["esito"] == "SCORPORA"
        assert r["fv_separato_eur"] == -12000.0

    def test_scorpora_derivato_valutario(self):
        r = _F["mh530_misura"](_c(tipo="derivato_valutario", rif="USD"))
        assert r["esito"] == "SCORPORA"

    def test_nessuno_scorporo_correlato(self):
        # gas indicizzato TTF: stessa commodity -> correlato
        r = _F["mh530_misura"](_c(rif="TTF", corr=True, fvi=0.0))
        assert r["esito"] == "NESSUNO_SCORPORO"
        assert r["fv_separato_eur"] == 0.0

    def test_nessuno_scorporo_cap_floor_correlato(self):
        r = _F["mh530_misura"](_c(tipo="opzione_cap_floor",
                                  rif="prezzo power", host="power",
                                  corr=True))
        assert r["esito"] == "NESSUNO_SCORPORO"

    def test_nessuno_scorporo_non_derivato_autonomo(self):
        r = _F["mh530_misura"](_c(auto=False))
        assert r["esito"] == "NESSUNO_SCORPORO"

    def test_nessuno_scorporo_ibrido_al_fvtpl(self):
        # l'ibrido al FVTPL prevale anche con rischi non correlati
        r = _F["mh530_misura"](_c(fv=True, corr=False))
        assert r["esito"] == "NESSUNO_SCORPORO"


class TestW530Riepilogo:
    def test_tutti_scorporati(self):
        r = _F["mh530_riepilogo"]([_c("A"), _c("B", fvi=-5000.0)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_SCORPORATI"
        assert t["n_scorporati"] == 2
        assert t["fv_separato_totale_eur"] == 40000.0
        assert t["fv_separato_medio_eur"] == 20000.0

    def test_nessuno_scorporo(self):
        r = _F["mh530_riepilogo"]([_c("A", corr=True, fvi=0.0)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "NESSUNO_SCORPORO"
        assert t["fv_separato_totale_eur"] == 0.0
        assert t["fv_separato_medio_eur"] == 0.0

    def test_misto(self):
        r = _F["mh530_riepilogo"]([_c("A"), _c("B", corr=True, fvi=0.0),
                                   _c("C", fv=True)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "MISTO"
        assert t["n_contratti"] == 3 and t["n_scorporati"] == 1
        assert t["n_nessuno_scorporo"] == 2
        assert t["fv_separato_totale_eur"] == 45000.0
        assert t["fv_separato_medio_eur"] == 45000.0

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh530_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh530_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh530_riepilogo"]([_c("A"), _c("A")])


def test_registry_tab530():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 540
    assert TITLE530 in titoli
    assert TITLE529 in titoli
    assert src.count(TITLE530) == 3
    assert ", tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540 = st.tabs([" in src
    # chiavi widget st530_* univoche (10+ pattern attesi)
    keys = re.findall(r'key=f?"(st530_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 10
