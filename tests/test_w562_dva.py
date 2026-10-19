"""Test tab562 'DVA: debit valuation adjustment del portafoglio': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh562_num", "mh562_str", "mh562_ge0", "mh562_bps",
           "mh562_csa", "mh562_netting", "mh562_demo",
           "mh562_riepilogo")

TITLE562 = ("\U0001F4B3\U0001F4CA DVA: debit valuation adjustment "
            "del portafoglio")


def _e6(*vals):
    vals = list(vals) + [0.0] * (6 - len(vals))
    return tuple(vals[:6])


def _v(nid="D-1", cp="CP", ene=None, sp=100.0, ta=0.0, csa="CSA_NO"):
    return _F["mh562_netting"](
        nid, cp, _e6(*(ene or (1000000.0,))), sp, ta, csa)


class TestW562Validatori:
    def test_num_ok(self):
        assert _F["mh562_num"](2, "x") == 2.0
        assert _F["mh562_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf, -0.01):
            with pytest.raises(ValueError):
                _F["mh562_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh562_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh562_str"](bad, "x")

    def test_bps_ok(self):
        assert _F["mh562_bps"](10000.0) == 10000.0

    def test_bps_ko(self):
        for bad in (10000.01, -1.0, "x"):
            with pytest.raises(ValueError):
                _F["mh562_bps"](bad)

    def test_csa_ok(self):
        assert _F["mh562_csa"]("csa_si") == "CSA_SI"
        assert _F["mh562_csa"]("CSA_NO") == "CSA_NO"

    def test_csa_ko(self):
        for bad in ("SI", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh562_csa"](bad)


class TestW562Netting:
    def test_voce_semplice(self):
        # 1M su fascia 0-3M, spread 100bps=1%, r=0:
        # DVA = 1e6 * 0.01 * 0.25 * 1.0 = 2500
        v = _v()
        assert v["ene_totale"] == 1000000.0
        assert v["dva_lordo"] == pytest.approx(2500.0)
        assert v["dva"] == pytest.approx(2500.0)
        assert v["csa"] == "CSA_NO"

    def test_csa_dimezza(self):
        v = _v(csa="CSA_SI")
        assert v["dva_lordo"] == pytest.approx(2500.0)
        assert v["dva"] == pytest.approx(1250.0)

    def test_sconto_riduce(self):
        v0 = _v(ta=0.0)
        v5 = _v(ta=5.0)
        assert v5["dva"] < v0["dva"]
        assert v5["dva"] == pytest.approx(
            2500.0 * 1.05 ** -0.125)

    def test_ene_sei_fasce(self):
        with pytest.raises(ValueError):
            _F["mh562_netting"]("D-9", "CP", (1.0, 2.0, 3.0),
                                100.0, 0.0, "CSA_NO")

    def test_ene_negativa(self):
        with pytest.raises(ValueError):
            _v(ene=(-1.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    def test_spread_max(self):
        with pytest.raises(ValueError):
            _v(sp=10001.0)


class TestW562Riepilogo:
    def test_demo(self):
        d = _F["mh562_demo"]()
        assert len(d) == 3
        r = _F["mh562_riepilogo"](d)
        assert r["n_netting"] == 3
        assert r["n_anomalie"] == 0
        assert r["ene_totale"] == pytest.approx(40000000.0)
        assert [round(x["dva_lordo"], 2) for x in d] == [
            pytest.approx(104701.67, abs=0.01),
            pytest.approx(112561.28, abs=0.01),
            pytest.approx(16305.57, abs=0.01)]
        # DVA-002 ha CSA_SI -> dimezzato
        assert d[1]["dva"] == pytest.approx(d[1]["dva_lordo"] / 2.0)
        assert r["verdetto"] == "DVA_CONTENUTO"
        assert r["dva_su_ene"] == pytest.approx(
            r["dva_totale"] / 40000000.0)
        assert r["dva_su_ene"] < 0.02

    def test_demo_deterministica(self):
        assert _F["mh562_demo"]() == _F["mh562_demo"]()

    def test_significativo(self):
        # spread 10000bps=100% su 1M fascia 0-3M, r=0 -> DVA 250k, ratio 25%
        r = _F["mh562_riepilogo"]([_v(sp=10000.0)])
        assert r["verdetto"] == "DVA_SIGNIFICATIVO"
        assert r["dva_su_ene"] == pytest.approx(0.25)

    def test_id_duplicato(self):
        r = _F["mh562_riepilogo"]([_v("DUP"), _v("dup")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a.lower()
                   for a in r["analizzati"][1]["anomalie"])

    def test_ene_nulla(self):
        r = _F["mh562_riepilogo"]([_v(ene=(0.0,) * 6), _v("D-2")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nullo" in a.lower() or "nulla" in a.lower()
                   for a in r["analizzati"][0]["anomalie"])

    def test_spread_nullo(self):
        r = _F["mh562_riepilogo"]([_v(sp=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("spread" in a.lower()
                   for a in r["analizzati"][0]["anomalie"])

    def test_nessuna_esposizione(self):
        r = _F["mh562_riepilogo"]([_v(ene=(0.0,) * 6, sp=0.0)])
        assert r["verdetto"] == "NESSUNA_ESPOSIZIONE"
        assert r["dva_totale"] == 0.0

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh562_riepilogo"]([])


class TestW562Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_562_presente(self):
        assert self._src().count(TITLE562) == 3

    def test_counts_562(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 570
        assert TITLE562 in titoli
        assert "tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570 = st.tabs([" in src

    def test_chiavi_562_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st562_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st562_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
