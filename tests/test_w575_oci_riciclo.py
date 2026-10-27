"""Test tab575 "Importi a OCI e riciclo a P&L (IFRS 7.24E)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh575_num", "mh575_str", "mh575_tipo",
           "mh575_relazione", "mh575_demo", "mh575_riepilogo")

TITLE575 = "📊🔄 Importi a OCI e riciclo a P&L (IFRS 7.24E)"


def _r(rid="HED-1", descrizione="relazione", tipo="CASH_FLOW",
       oci=-450_000.0, rp=-300_000.0, ba=-50_000.0):
    return _F["mh575_relazione"](rid, descrizione, tipo, oci,
                                 riciclo_pl=rp, basis_adj=ba)


class TestW575Validatori:
    def test_num_ok(self):
        assert _F["mh575_num"](2, "x") == 2.0
        assert _F["mh575_num"](-3.5, "x") == -3.5
        assert _F["mh575_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh575_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh575_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh575_str"](bad, "x")

    def test_tipo_ok(self):
        assert _F["mh575_tipo"]("fair_value") == "FAIR_VALUE"
        assert _F["mh575_tipo"]("Cash Flow") == "CASH_FLOW"
        assert _F["mh575_tipo"]("NET_INVESTMENT") == "NET_INVESTMENT"

    def test_tipo_ko(self):
        for bad in ("FV", "", None, "cashflow"):
            with pytest.raises(ValueError):
                _F["mh575_tipo"](bad)


class TestW575Relazione:
    def test_cfh_hand_computed(self):
        r = _r()
        assert r["var_oci"] == pytest.approx(-450_000.0)
        assert r["riciclo_pl"] == pytest.approx(-300_000.0)
        assert r["basis_adj"] == pytest.approx(-50_000.0)
        assert r["impatto_pl"] == pytest.approx(-300_000.0)
        assert r["completa"] and r["anomalie"] == []

    def test_cfh_riciclo_mancante_anomalia(self):
        r = _F["mh575_relazione"]("HED-1", "r", "CASH_FLOW", -100.0,
                                  riciclo_pl=None, basis_adj=0.0)
        assert not r["completa"]
        assert any("riciclato a P&L non dichiarato" in a
                   for a in r["anomalie"])

    def test_cfh_basis_none_default_zero(self):
        r = _F["mh575_relazione"]("HED-1", "r", "CASH_FLOW", -100.0,
                                  riciclo_pl=0.0, basis_adj=None)
        assert r["basis_adj"] == 0.0
        assert r["completa"]

    def test_fv_ok(self):
        r = _F["mh575_relazione"]("HED-FV", "irs", "FAIR_VALUE", 0.0)
        assert r["completa"]

    def test_fv_oci_nonzero_anomalia(self):
        r = _F["mh575_relazione"]("HED-FV", "irs", "FAIR_VALUE", 5_000.0)
        assert not r["completa"]
        assert any("variazione a OCI non attesa" in a
                   for a in r["anomalie"])

    def test_fv_componenti_oci_anomalia(self):
        r = _F["mh575_relazione"]("HED-FV", "irs", "FAIR_VALUE", 0.0,
                                  riciclo_pl=10.0)
        assert any("riciclo OCI non attesa" in a
                   for a in r["anomalie"])

    def test_ni_ok(self):
        r = _F["mh575_relazione"]("HED-NI", "hedge", "NET_INVESTMENT",
                                  -250_000.0, riciclo_pl=-250_000.0,
                                  basis_adj=None)
        assert r["completa"]

    def test_ni_basis_anomalia(self):
        r = _F["mh575_relazione"]("HED-NI", "hedge", "NET_INVESTMENT",
                                  -250_000.0, riciclo_pl=-250_000.0,
                                  basis_adj=0.0)
        assert any("Basis adjustment non applicabile" in a
                   for a in r["anomalie"])

    def test_ni_riciclo_mancante_anomalia(self):
        r = _F["mh575_relazione"]("HED-NI", "hedge", "NET_INVESTMENT",
                                  -250_000.0)
        assert not r["completa"]

    def test_str_strip(self):
        r = _F["mh575_relazione"]("  HED-X  ", "  d  ", "cash_flow",
                                  0.0, riciclo_pl=0.0)
        assert r["id"] == "HED-X"
        assert r["tipo"] == "CASH_FLOW"

    def test_oci_non_numero_ko(self):
        with pytest.raises(ValueError):
            _F["mh575_relazione"]("HED-1", "r", "CASH_FLOW", "x",
                                  riciclo_pl=0.0)


class TestW575Riepilogo:
    def test_demo_riciclo_significativo(self):
        r = _F["mh575_riepilogo"](_F["mh575_demo"]())
        # oci = -1850k + 210k = -1_640_000
        # riciclo = -1620k + 180k = -1_440_000
        # basis = -120k; riserva = -1640k + 1440k + 120k = -80_000
        assert r["totale_oci"] == pytest.approx(-1_640_000.0)
        assert r["totale_riciclo"] == pytest.approx(-1_440_000.0)
        assert r["totale_basis"] == pytest.approx(-120_000.0)
        assert r["variazione_riserva"] == pytest.approx(-80_000.0)
        assert r["n_relazioni"] == 3
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "RICICLO_SIGNIFICATIVO"
        assert r["maggiore_riciclo_id"] == "HED-101"
        assert r["oci_per_tipo"]["Cash flow hedges"] == \
            pytest.approx(-1_640_000.0)
        assert r["riciclo_per_tipo"]["Fair value hedges"] == \
            pytest.approx(0.0)

    def test_oci_gestibile(self):
        r = _F["mh575_riepilogo"]([_r()], soglia_eur=1_000_000.0)
        assert r["verdetto"] == "OCI_GESTIBILE"

    def test_nessuna_relazione(self):
        r = _F["mh575_riepilogo"]([])
        assert r["verdetto"] == "NESSUNA_RELAZIONE"
        assert r["n_relazioni"] == 0
        assert r["oci_per_tipo"]["Cash flow hedges"] == 0.0

    def test_duplicati_anomalia(self):
        r = _F["mh575_riepilogo"]([_r(rid="DUP"), _r(rid="DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all("ID duplicato" in x["anomalie"] for x in r["analizzate"])

    def test_anomalie_hanno_priorita(self):
        # riciclo sopra soglia MA con anomalia -> ANOMALIE_DA_VERIFICARE
        bad = _F["mh575_relazione"]("HED-B", "r", "CASH_FLOW",
                                    -100.0, riciclo_pl=None)
        r = _F["mh575_riepilogo"]([bad], soglia_eur=10.0)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh575_riepilogo"]([_r()], soglia_eur=0.0)

    def test_maggiore_riciclo_none_se_tutto_zero(self):
        r = _F["mh575_riepilogo"](
            [_F["mh575_relazione"]("HED-0", "zero", "CASH_FLOW", 0.0,
                                   riciclo_pl=0.0)])
        assert r["maggiore_riciclo_id"] is None
        assert r["verdetto"] == "OCI_GESTIBILE"


class TestW575Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE575}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 753
        assert TITLE575 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753 = st.tabs([" in src
        assert "with tab575:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st575_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
