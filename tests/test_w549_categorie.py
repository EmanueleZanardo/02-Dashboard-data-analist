"""Test tab549 'Valore contabile per categoria (IFRS 7.8)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh549_num", "mh549_str", "mh549_lato", "mh549_categoria",
           "mh549_voce", "mh549_demo", "mh549_riepilogo")

TITLE549 = "\U0001f9fe\U0001f4ca Valore contabile per categoria (IFRS 7.8)"


def _v(vid="V-1", d="x", lato="ATTIVO", cat="COSTO_AMMORTIZZATO", vc=1000.0):
    return {"id": vid, "descrizione": d, "lato": lato, "categoria": cat,
            "valore_contabile": vc}


class TestW549Validatori:
    def test_num_ok(self):
        assert _F["mh549_num"](2, "x") == 2.0
        assert _F["mh549_num"](0, "x") == 0.0
        assert _F["mh549_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh549_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh549_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh549_str"](bad, "x")

    def test_lato_ok_ko(self):
        assert _F["mh549_lato"]("ATTIVO", "x") == "ATTIVO"
        assert _F["mh549_lato"]("PASSIVO", "x") == "PASSIVO"
        for bad in ("attivo", "ATTIVI", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh549_lato"](bad, "x")

    def test_categoria_ok_ko(self):
        for ok in ("FVTPL_TRADING", "FVTPL_DESIGNATO", "FVOCI",
                   "COSTO_AMMORTIZZATO"):
            assert _F["mh549_categoria"](ok, "x") == ok
        for bad in ("FVTPL", "fvoci", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh549_categoria"](bad, "x")


class TestW549Voce:
    def test_voce_ok(self):
        o = _F["mh549_voce"](_v())
        assert o["id"] == "V-1"
        assert o["lato"] == "ATTIVO"
        assert o["categoria"] == "COSTO_AMMORTIZZATO"
        assert o["valore_contabile"] == 1000.0
        assert o["anomalie"] == []

    def test_anomalia_fvoci_passivo(self):
        o = _F["mh549_voce"](_v(lato="PASSIVO", cat="FVOCI"))
        assert any("FVOCI" in a for a in o["anomalie"])

    def test_fvoci_attivo_ok(self):
        o = _F["mh549_voce"](_v(lato="ATTIVO", cat="FVOCI"))
        assert o["anomalie"] == []

    def test_anomalia_vc_zero(self):
        o = _F["mh549_voce"](_v(vc=0.0))
        assert any("nullo" in a for a in o["anomalie"])

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh549_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh549_voce"]({"id": "A"})
        with pytest.raises(ValueError):
            _F["mh549_voce"](_v(vc=-1.0))
        with pytest.raises(ValueError):
            _F["mh549_voce"](_v(lato="X"))
        with pytest.raises(ValueError):
            _F["mh549_voce"](_v(cat="X"))
        with pytest.raises(ValueError):
            _F["mh549_voce"](_v(vid=""))


class TestW549Demo:
    def test_demo_verdetto(self):
        demo = _F["mh549_demo"]()
        assert len(demo) == 4
        assert [r["id"] for r in demo] == ["PPA-DE-001", "FIN-IT-002",
                                          "CRD-IT-003", "EQO-IT-004"]
        ri = _F["mh549_riepilogo"](demo)
        assert ri["attivo_tot"] == pytest.approx(47000000.0)
        assert ri["passivo_tot"] == pytest.approx(45000000.0)
        assert ri["netto"] == pytest.approx(2000000.0)
        assert ri["quota_fvtpl_attivo"] == pytest.approx(12000000.0 /
                                                        47000000.0)
        assert ri["verdetto"] == "FVTPL_SIGNIFICATIVO"
        assert ri["n_anomalie"] == 0
        assert ri["per_categoria"]["FVTPL_TRADING"]["attivo"] == \
            pytest.approx(12000000.0)
        assert ri["per_categoria"]["COSTO_AMMORTIZZATO"]["n"] == 2
        assert ri["per_categoria"]["COSTO_AMMORTIZZATO"]["passivo"] == \
            pytest.approx(45000000.0)

    def test_demo_deterministico(self):
        assert _F["mh549_demo"]() == _F["mh549_demo"]()


class TestW549Riepilogo:
    def test_verdetto_anomalia(self):
        ri = _F["mh549_riepilogo"]([_v(vid="A", lato="PASSIVO",
                                       cat="FVOCI", vc=1000.0)])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert ri["n_anomalie"] == 1

    def test_verdetto_concentrato_boundary(self):
        base = [_v(vid="B", cat="COSTO_AMMORTIZZATO", vc=700.0)]
        ri = _F["mh549_riepilogo"](
            [_v(vid="A", cat="FVTPL_TRADING", vc=300.0)] + base)
        assert ri["quota_fvtpl_attivo"] == pytest.approx(0.30)
        assert ri["verdetto"] == "FVTPL_SIGNIFICATIVO"
        ri2 = _F["mh549_riepilogo"](
            [_v(vid="A", cat="FVTPL_TRADING", vc=301.0)] + base)
        assert ri2["verdetto"] == "FVTPL_CONCENTRATO"

    def test_verdetto_significativo_boundary(self):
        base = [_v(vid="B", cat="COSTO_AMMORTIZZATO", vc=900.0)]
        ri = _F["mh549_riepilogo"](
            [_v(vid="A", cat="FVTPL_DESIGNATO", vc=100.0)] + base)
        assert ri["quota_fvtpl_attivo"] == pytest.approx(0.10)
        assert ri["verdetto"] == "CATEGORIE_BILANCIATE"
        ri2 = _F["mh549_riepilogo"](
            [_v(vid="A", cat="FVTPL_DESIGNATO", vc=100.01)] + base)
        assert ri2["verdetto"] == "FVTPL_SIGNIFICATIVO"

    def test_nessuna_voce(self):
        ri = _F["mh549_riepilogo"]([_v(vid="A", vc=0.0)])
        assert ri["verdetto"] == "NESSUNA_VOCE"

    def test_per_categoria(self):
        ri = _F["mh549_riepilogo"](
            [_v(vid="A", lato="ATTIVO", cat="FVTPL_TRADING", vc=800.0),
             _v(vid="B", lato="PASSIVO", cat="FVTPL_TRADING", vc=200.0),
             _v(vid="C", lato="ATTIVO", cat="FVOCI", vc=500.0)])
        assert set(ri["per_categoria"]) == {"FVTPL_TRADING", "FVOCI"}
        assert ri["per_categoria"]["FVTPL_TRADING"]["attivo"] == \
            pytest.approx(800.0)
        assert ri["per_categoria"]["FVTPL_TRADING"]["passivo"] == \
            pytest.approx(200.0)
        assert ri["per_categoria"]["FVTPL_TRADING"]["n"] == 2
        assert ri["quota_fvtpl_passivo"] == pytest.approx(1.0)

    def test_soglie_custom(self):
        demo = _F["mh549_demo"]()
        ri = _F["mh549_riepilogo"](demo, soglia_sig=0.50, soglia_conc=0.60)
        assert ri["verdetto"] == "CATEGORIE_BILANCIATE"
        ri2 = _F["mh549_riepilogo"](demo, soglia_sig=0.20, soglia_conc=0.25)
        assert ri2["verdetto"] == "FVTPL_CONCENTRATO"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]("non-lista")
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]([_v()], soglia_sig=0.3, soglia_conc=0.3)
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]([_v()], soglia_sig=0.4, soglia_conc=0.3)
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]([_v()], soglia_sig=0.0, soglia_conc=0.5)
        with pytest.raises(ValueError):
            _F["mh549_riepilogo"]([_v()], soglia_sig=True, soglia_conc=0.5)

    def test_fvtpl_passivo_non_in_quota_attivo(self):
        ri = _F["mh549_riepilogo"](
            [_v(vid="A", lato="PASSIVO", cat="FVTPL_TRADING", vc=5000.0),
             _v(vid="B", lato="PASSIVO", cat="COSTO_AMMORTIZZATO",
                vc=5000.0)])
        assert ri["quota_fvtpl_attivo"] == pytest.approx(0.0)
        assert ri["verdetto"] == "CATEGORIE_BILANCIATE"


class TestW549Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_titolo_549_presente(self):
        assert self._src().count(TITLE549) == 3

    def test_counts_549(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 667
        assert TITLE549 in titoli

    def test_ui_indentata(self):
        assert "    with tab549:" in self._src()

    def test_dvar_line(self):
        assert "tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667 = st.tabs([" in self._src()

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st549_" in ln]
        # le f-string st549_id_{_i549} generano istanze a runtime: la base
        # e' fino al suffisso numerico; csv1/csv2 sono chiavi distinte
        basi = [re.search(r"st549_[a-z]+\d*", ln).group(0)
                for ln in righe]
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
