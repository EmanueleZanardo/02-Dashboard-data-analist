"""Test tab529 '⚖️⏹️ Cessazione hedge accounting (IFRS 9 6.5.12)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh529_num", "mh529_str", "mh529_relazione",
           "mh529_misura", "mh529_riepilogo")

TITLE529 = "⚖️⏹️ Cessazione hedge accounting (IFRS 9 6.5.12)"
TITLE528 = "⚖️🔌 Own-use exemption NPNS (IFRS 9 2.4)"


def _r(rid="R-1", tipo="cash_flow",
       causa="item_non_piu_qualifica",
       ris=85000.0, ade=0.0, d="x"):
    return {"id": rid, "tipo_copertura": tipo, "causa": causa,
            "riserva_oci_eur": ris, "adeguamento_fv_eur": ade,
            "descrizione": d}


class TestW529Validatori:
    def test_num_ok(self):
        assert _F["mh529_num"](2, "x") == 2.0
        assert _F["mh529_num"](-1.5, "x") == -1.5
        assert _F["mh529_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh529_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh529_str"]("  R-1 ", "x") == "R-1"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh529_str"](bad, "x")


class TestW529Relazione:
    def test_ok_normalizza(self):
        r = _F["mh529_relazione"](_r())
        assert r["id"] == "R-1"
        assert r["tipo_copertura"] == "cash_flow"
        assert r["riserva_oci_eur"] == 85000.0
        assert r["descrizione"] == "x"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh529_relazione"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh529_relazione"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(rid="  "))
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(tipo="trading"))
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(causa="boh"))
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(ris=True))
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(ade=math.nan))
        with pytest.raises(ValueError):
            _F["mh529_relazione"](_r(ris=math.inf))
        v = _r()
        v["descrizione"] = 7
        with pytest.raises(ValueError):
            _F["mh529_relazione"](v)


class TestW529Misura:
    def test_riserva_in_oci_probabile(self):
        r = _F["mh529_misura"](_r())
        assert r["esito"] == "RISERVA_IN_OCI"
        assert r["riserva_oci_eur"] == 85000.0
        assert r["pnl_subito_eur"] == 0.0
        assert r["adeguamento_da_ammortizzare_eur"] == 0.0

    def test_rileva_subito_forecast_non_attesa(self):
        r = _F["mh529_misura"](_r(causa="forecast_non_piu_attesa",
                                  ris=-30000.0))
        assert r["esito"] == "RILEVA_SUBITO"
        assert r["pnl_subito_eur"] == -30000.0
        assert r["riserva_oci_eur"] == 0.0

    def test_rileva_subito_solo_cash_flow(self):
        # forecast non piu' attesa su fair value -> AMMORTIZZA
        r = _F["mh529_misura"](_r(tipo="fair_value",
                                  causa="forecast_non_piu_attesa",
                                  ade=120000.0))
        assert r["esito"] == "AMMORTIZZA"

    def test_ammortizza_fair_value(self):
        r = _F["mh529_misura"](_r(tipo="fair_value",
                                  causa="strumento_scaduto_venduto_risolto",
                                  ade=120000.0))
        assert r["esito"] == "AMMORTIZZA"
        assert r["adeguamento_da_ammortizzare_eur"] == 120000.0
        assert r["pnl_subito_eur"] == 0.0

    def test_ammortizza_obiettivo_cambiato(self):
        r = _F["mh529_misura"](_r(tipo="fair_value",
                                  causa="obiettivo_gestione_cambiato",
                                  ade=50000.0))
        assert r["esito"] == "AMMORTIZZA"
        assert r["adeguamento_da_ammortizzare_eur"] == 50000.0

    def test_net_investment_in_oci(self):
        r = _F["mh529_misura"](_r(tipo="net_investment",
                                  causa="strumento_scaduto_venduto_risolto",
                                  ris=200000.0))
        assert r["esito"] == "RISERVA_IN_OCI"
        assert r["riserva_oci_eur"] == 200000.0

    def test_nessuna_cessazione_rollover(self):
        r = _F["mh529_misura"](_r(causa="rollover_continuazione",
                                  ris=85000.0))
        assert r["esito"] == "NESSUNA_CESSAZIONE"
        assert r["pnl_subito_eur"] == 0.0
        assert r["riserva_oci_eur"] == 0.0
        assert r["adeguamento_da_ammortizzare_eur"] == 0.0


class TestW529Riepilogo:
    def test_tutti_rileva_subito(self):
        r = _F["mh529_riepilogo"]([_r("A", causa="forecast_non_piu_attesa",
                                       ris=-30000.0),
                                   _r("B", causa="forecast_non_piu_attesa",
                                       ris=10000.0)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_RILEVATI_SUBITO"
        assert t["n_rileva_subito"] == 2
        assert t["pnl_subito_eur"] == -20000.0

    def test_tutti_in_oci(self):
        r = _F["mh529_riepilogo"]([_r("A"), _r("B", ris=15000.0)])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_IN_OCI"
        assert t["riserva_oci_trattenuta_eur"] == 100000.0

    def test_nessuna_cessazione(self):
        r = _F["mh529_riepilogo"]([_r("A", causa="rollover_continuazione")])
        assert r["totali"]["verdetto_complessivo"] == "NESSUNA_CESSAZIONE"

    def test_misto(self):
        r = _F["mh529_riepilogo"]([_r("A", tipo="fair_value",
                                       causa="obiettivo_gestione_cambiato",
                                       ade=50000.0),
                                   _r("B", causa="forecast_non_piu_attesa",
                                       ris=-30000.0),
                                   _r("C", causa="rollover_continuazione")])
        t = r["totali"]
        assert t["verdetto_complessivo"] == "MISTO"
        assert t["n_relazioni"] == 3 and t["n_continuano"] == 1
        assert t["pnl_subito_eur"] == -30000.0
        assert t["adeguamento_da_ammortizzare_eur"] == 50000.0
        assert t["riserva_oci_trattenuta_eur"] == 0.0

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh529_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh529_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh529_riepilogo"]([_r("A"), _r("A")])


def test_registry_tab529():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 752
    assert TITLE529 in titoli
    assert TITLE528 in titoli
    assert src.count(TITLE529) == 3
    assert ", tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752 = st.tabs([" in src
    # chiavi widget st529_* univoche (10 pattern attesi)
    keys = re.findall(r'key=f?"(st529_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 10
