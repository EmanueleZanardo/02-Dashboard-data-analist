"""Test tab532 '🧾💸 SPPI test (IFRS 9 4.1.2(b))': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh532_num", "mh532_str", "mh532_bool", "mh532_strumento",
           "mh532_sppi", "mh532_riepilogo")

TITLE532 = "🧾💸 SPPI test (IFRS 9 4.1.2(b))"
TITLE531 = "⚖️📶 Gerarchia fair value (IFRS 13)"


def _s(cid="S-1", tipo="prestito", tasso="fisso", leva=False, lec=False,
       conv=False, pnp=False, rlp=False, cap=1000000.0, d="x"):
    return {"id": cid, "tipo_strumento": tipo, "struttura_tasso": tasso,
            "leva": leva, "legato_equity_commodity": lec,
            "conversione_azionaria": conv, "prepayment_non_par": pnp,
            "recourse_limitato_progetto": rlp, "capitale_eur": cap,
            "descrizione": d}


class TestW532Validatori:
    def test_num_ok(self):
        assert _F["mh532_num"](2, "x") == 2.0
        assert _F["mh532_num"](-1.5, "x") == -1.5
        assert _F["mh532_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh532_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh532_str"]("  S-1 ", "x") == "S-1"

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh532_str"](bad, "x")

    def test_bool_ok(self):
        assert _F["mh532_bool"](True, "x") is True
        assert _F["mh532_bool"](False, "x") is False

    def test_bool_ko(self):
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh532_bool"](bad, "x")


class TestW532Strumento:
    def test_strumento_ok(self):
        s = _F["mh532_strumento"](_s(cid=" CRED-1 "))
        assert s["id"] == "CRED-1"
        assert s["capitale_eur"] == 1000000.0
        assert s["struttura_tasso"] == "fisso"

    def test_strumento_chiave_mancante(self):
        v = _s()
        del v["capitale_eur"]
        with pytest.raises(ValueError):
            _F["mh532_strumento"](v)

    def test_strumento_ko(self):
        with pytest.raises(ValueError):
            _F["mh532_strumento"]("no")
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(tipo="future"))
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(tasso="step-up"))
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(cap=-5.0))
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(leva=1))
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(cid="  "))
        with pytest.raises(ValueError):
            _F["mh532_strumento"](_s(d=""))


class TestW532Sppi:
    def test_superato_prestito_fisso(self):
        r = _F["mh532_sppi"](_s())
        assert r["esito"] == "SPPI_SUPERATO"
        assert r["categoria_contabile"] == "COSTO_AMMORTIZZATO"
        assert r["capitale_eur"] == 1000000.0

    def test_superato_variabile_e_zero_coupon(self):
        for tasso in ("variabile", "zero_coupon"):
            r = _F["mh532_sppi"](_s(tasso=tasso))
            assert r["esito"] == "SPPI_SUPERATO"

    def test_fallito_leva(self):
        r = _F["mh532_sppi"](_s(cid="L", leva=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert r["categoria_contabile"] == "FVTPL"
        assert "leva" in r["motivo"]

    def test_fallito_legato_commodity(self):
        r = _F["mh532_sppi"](_s(cid="C", lec=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert "commodity" in r["motivo"]

    def test_fallito_conversione(self):
        r = _F["mh532_sppi"](_s(cid="V", conv=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert "equity" in r["motivo"]

    def test_fallito_prepayment(self):
        r = _F["mh532_sppi"](_s(cid="P", pnp=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert "prepayment" in r["motivo"]

    def test_fallito_non_recourse(self):
        r = _F["mh532_sppi"](_s(cid="R", rlp=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert "non-recourse" in r["motivo"]

    def test_priorita_prima_clausola(self):
        r = _F["mh532_sppi"](_s(cid="M", leva=True, lec=True, conv=True,
                                pnp=True, rlp=True))
        assert r["esito"] == "SPPI_FALLITO"
        assert "leva" in r["motivo"]

    def test_boundary_capitale_zero(self):
        r = _F["mh532_sppi"](_s(cap=0.0))
        assert r["esito"] == "SPPI_SUPERATO"
        assert r["capitale_eur"] == 0.0


class TestW532Riepilogo:
    def test_tutti_sppi(self):
        r = _F["mh532_riepilogo"]([_s(cid="A"), _s(cid="B", cap=500000.0)])
        t = r["totali"]
        assert t["verdetto"] == "TUTTI_SPPI"
        assert t["n_strumenti"] == 2
        assert t["n_sppi"] == 2 and t["n_falliti"] == 0
        assert t["capitale_totale_eur"] == 1500000.0
        assert t["capitale_fvtpl_eur"] == 0.0
        assert t["pct_capitale_fvtpl"] == 0.0

    def test_alcuni_falliti(self):
        r = _F["mh532_riepilogo"]([_s(cid="A"), _s(cid="B", leva=True,
                                                     cap=500000.0)])
        t = r["totali"]
        assert t["verdetto"] == "ALCUNI_FALLITI"
        assert t["n_sppi"] == 1 and t["n_falliti"] == 1
        assert t["capitale_sppi_eur"] == 1000000.0
        assert t["capitale_fvtpl_eur"] == 500000.0
        assert t["pct_capitale_fvtpl"] == pytest.approx(33.3333, abs=1e-3)
        assert [x["esito"] for x in r["righe"]] == ["SPPI_SUPERATO",
                                                   "SPPI_FALLITO"]

    def test_tutti_falliti(self):
        r = _F["mh532_riepilogo"]([_s(cid="A", lec=True),
                                   _s(cid="B", rlp=True, cap=2000000.0)])
        t = r["totali"]
        assert t["verdetto"] == "TUTTI_FALLITI"
        assert t["capitale_fvtpl_eur"] == 3000000.0
        assert t["pct_capitale_fvtpl"] == 100.0

    def test_id_duplicato(self):
        with pytest.raises(ValueError):
            _F["mh532_riepilogo"]([_s(cid="A"), _s(cid="A")])

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh532_riepilogo"]([])

    def test_non_lista(self):
        with pytest.raises(ValueError):
            _F["mh532_riepilogo"]("no")


class TestW532Registry:
    def test_titolo_532_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE532) == 3

    def test_registry_tab_count_532(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 784
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 784

    def test_tab532_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784 = st.tabs([" in src
        assert "with tab532:" in src

    def test_chiavi_st532_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st532_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
