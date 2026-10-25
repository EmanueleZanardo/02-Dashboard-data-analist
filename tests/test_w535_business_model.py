"""Test tab535 '🏦📋 Business model assessment (IFRS 9 4.1.1/4.1.2(a))': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh535_num", "mh535_pct", "mh535_str", "mh535_bool",
           "mh535_int0", "mh535_portafoglio", "mh535_classifica",
           "mh535_riepilogo")

TITLE535 = "🏦📋 Business model assessment (IFRS 9 4.1.1/4.1.2(a))"
TITLE534 = "📐📊 Tasso di interesse effettivo (IFRS 9 5.4.1)"


def _p(cid="P-1", mod="hold_to_collect", sppi=True, nv=0, quota=0.0,
       freq=False, det=False, sca=False, des=False, d="x"):
    return {"id": cid, "descrizione": d, "modello": mod,
            "sppi_superato": sppi, "vendite_annue": nv,
            "quota_vendite_pct": quota, "vendite_frequenti": freq,
            "vendite_solo_deterioramento_credito": det,
            "vendite_prossime_scadenza": sca,
            "designa_fvtpl_mismatch": des}


class TestW535Validatori:
    def test_num_ok(self):
        assert _F["mh535_num"](2, "x") == 2.0
        assert _F["mh535_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh535_num"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh535_pct"](0.0, "x") == 0.0
        assert _F["mh535_pct"](100.0, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "50", None):
            with pytest.raises(ValueError):
                _F["mh535_pct"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh535_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh535_bool"](True, "x") is True
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh535_bool"](bad, "x")

    def test_int0_ok(self):
        assert _F["mh535_int0"](0, "x") == 0
        assert _F["mh535_int0"](40, "x") == 40

    def test_int0_ko(self):
        for bad in (-1, 1.5, True, "3", None):
            with pytest.raises(ValueError):
                _F["mh535_int0"](bad, "x")


class TestW535Portafoglio:
    def test_ok(self):
        p = _F["mh535_portafoglio"](_p(cid=" P-1 "))
        assert p["id"] == "P-1"
        assert p["modello"] == "hold_to_collect"

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](["x"])

    def test_chiave_mancante(self):
        v = _p()
        del v["quota_vendite_pct"]
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](v)

    def test_modello_fuori_elenco(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(mod="hold_to_trade"))

    def test_quota_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(quota=100.1))

    def test_vendite_annue_ko(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(nv=-1))
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(nv=1.5))

    def test_flag_non_bool(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(sppi="si"))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh535_portafoglio"](_p(d=123))


class TestW535Classifica:
    def test_htc_nessuna_vendita(self):
        r = _F["mh535_classifica"](_p())
        assert r["esito"] == "COSTO_AMMORTIZZATO"
        assert r["coerenza_vendite"] == "coerente"

    def test_htc_vendite_deterioramento(self):
        r = _F["mh535_classifica"](_p(nv=3, quota=8.0, freq=True,
                                     det=True))
        assert r["esito"] == "COSTO_AMMORTIZZATO"

    def test_htc_vendite_prossime_scadenza(self):
        r = _F["mh535_classifica"](_p(nv=5, quota=20.0, freq=True,
                                     sca=True))
        assert r["esito"] == "COSTO_AMMORTIZZATO"

    def test_htc_infrequenti_significative(self):
        r = _F["mh535_classifica"](_p(nv=1, quota=30.0, freq=False))
        assert r["esito"] == "COSTO_AMMORTIZZATO"

    def test_htc_frequenti_insignificanti(self):
        r = _F["mh535_classifica"](_p(nv=12, quota=5.0, freq=True))
        assert r["esito"] == "COSTO_AMMORTIZZATO"

    def test_htc_incoerente_frequenti_e_significative(self):
        r = _F["mh535_classifica"](_p(nv=12, quota=5.1, freq=True))
        assert r["esito"] == "FVTPL"
        assert r["coerenza_vendite"] == "incoerente"

    def test_htcs(self):
        r = _F["mh535_classifica"](_p(mod="hold_to_collect_and_sell",
                                      nv=6, quota=12.0, freq=True))
        assert r["esito"] == "FVOCI"

    def test_other(self):
        r = _F["mh535_classifica"](_p(mod="altro_trading_fv", nv=40,
                                      quota=60.0, freq=True))
        assert r["esito"] == "FVTPL"
        assert r["coerenza_vendite"] == "n/a"

    def test_sppi_fallito_prevale_su_htc(self):
        r = _F["mh535_classifica"](_p(sppi=False))
        assert r["esito"] == "FVTPL"

    def test_designazione_prevale_su_tutto(self):
        r = _F["mh535_classifica"](_p(des=True))
        assert r["esito"] == "FVTPL"
        assert "4.1.5" in r["motivo"]


class TestW535Riepilogo:
    def _demo(self):
        return [_p(cid="PPA-REC-001", mod="hold_to_collect"),
                _p(cid="LIQ-BND-002",
                   mod="hold_to_collect_and_sell", nv=6, quota=12.0,
                   freq=True),
                _p(cid="TRD-COM-003", mod="altro_trading_fv", nv=40,
                   quota=60.0, freq=True)]

    def test_demo_misto(self):
        an = _F["mh535_riepilogo"](self._demo())
        tt = an["totali"]
        assert tt["verdetto"] == "MISTO"
        assert tt["n_costo_ammortizzato"] == 1
        assert tt["n_fvoci"] == 1
        assert tt["n_fvtpl"] == 1
        assert tt["n_portafogli"] == 3

    def test_tutti_costo_ammortizzato(self):
        an = _F["mh535_riepilogo"]([_p(cid="A"), _p(cid="B")])
        assert an["totali"]["verdetto"] == "TUTTI_COSTO_AMMORTIZZATO"

    def test_tutti_fvoci(self):
        an = _F["mh535_riepilogo"](
            [_p(cid="A", mod="hold_to_collect_and_sell"),
             _p(cid="B", mod="hold_to_collect_and_sell")])
        assert an["totali"]["verdetto"] == "TUTTI_FVOCI"

    def test_tutti_fvtpl(self):
        an = _F["mh535_riepilogo"](
            [_p(cid="A", mod="altro_trading_fv"),
             _p(cid="B", mod="altro_trading_fv")])
        assert an["totali"]["verdetto"] == "TUTTI_FVTPL"

    def test_id_duplicati(self):
        with pytest.raises(ValueError):
            _F["mh535_riepilogo"]([_p(cid="dup"), _p(cid="dup")])

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh535_riepilogo"]([])


class TestW535Registry:
    def test_titolo_535_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE535) == 3

    def test_registry_tab_count_535(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 699
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 699

    def test_tab535_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699 = st.tabs([" in src
        assert "with tab535:" in src

    def test_chiavi_st535_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st535_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
