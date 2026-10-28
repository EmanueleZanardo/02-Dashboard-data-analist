"""Test tab551 'Scadenze delle passività finanziarie (IFRS 7.39)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh551_num", "mh551_str", "mh551_categoria",
           "mh551_voce", "mh551_demo", "mh551_riepilogo")

TITLE551 = "💧📉 Scadenze delle passività finanziarie (IFRS 7.39)"


def _v(vid="V-1", d="x", cat="ALTRE_PASSIVITA", vc=1000000.0, imp=1200000.0,
       b1=300000.0, b2=300000.0, b3=400000.0, b4=200000.0, rl=True):
    return {"id": vid, "descrizione": d, "categoria": cat,
            "valore_contabile": vc, "importo_non_scontato": imp,
            "b1": b1, "b2": b2, "b3": b3, "b4": b4,
            "regolamento_lordo": rl}


class TestW551Validatori:
    def test_num_ok(self):
        assert _F["mh551_num"](2, "x") == 2.0
        assert _F["mh551_num"](0, "x") == 0.0
        assert _F["mh551_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh551_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh551_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh551_str"](bad, "x")

    def test_categoria_ok_ko(self):
        for ok in ("OBBLIGAZIONI_BOND", "FINANZIAMENTI_BANCARI",
                   "DEBITO_COMMERCIALE", "DERIVATI_PASSIVI",
                   "LEASING_IFRS16", "ALTRE_PASSIVITA"):
            assert _F["mh551_categoria"](ok) == ok
        for bad in ("ALTRO", "", None, 3, True):
            with pytest.raises(ValueError):
                _F["mh551_categoria"](bad)


class TestW551Voce:
    def test_voce_ok(self):
        o = _F["mh551_voce"](_v())
        assert o["somma_fasce"] == 1200000.0
        assert o["diff_riconciliazione"] == 0.0
        assert o["quota_breve"] == pytest.approx(0.25)
        assert o["anomalie"] == []

    def test_voce_riconciliazione(self):
        o = _F["mh551_voce"](_v(imp=1200000.0, b1=100000.0, b2=100000.0,
                                b3=100000.0, b4=100000.0))
        assert o["somma_fasce"] == 400000.0
        assert any("Somma fasce" in a for a in o["anomalie"])

    def test_voce_importo_minore_vc(self):
        o = _F["mh551_voce"](_v(vc=1000000.0, imp=900000.0, b1=900000.0,
                                b2=0.0, b3=0.0, b4=0.0))
        assert any("inferiore al valore contabile" in a
                   for a in o["anomalie"])

    def test_voce_vc_nullo(self):
        o = _F["mh551_voce"](_v(vc=0.0, imp=100000.0, b1=100000.0,
                                b2=0.0, b3=0.0, b4=0.0))
        assert any("Valore contabile nullo" in a for a in o["anomalie"])

    def test_voce_derivato_lordo(self):
        o = _F["mh551_voce"](_v(cat="DERIVATI_PASSIVI", vc=100000.0,
                                imp=100000.0, b1=100000.0, b2=0.0, b3=0.0,
                                b4=0.0, rl=False))
        assert any("regolamento netto" in a for a in o["anomalie"])
        o2 = _F["mh551_voce"](_v(cat="DERIVATI_PASSIVI", vc=100000.0,
                                 imp=100000.0, b1=100000.0, b2=0.0, b3=0.0,
                                 b4=0.0, rl=True))
        assert o2["anomalie"] == []

    def test_voce_bucket_vuoti(self):
        o = _F["mh551_voce"](_v(vc=100000.0, imp=100000.0, b1=0.0, b2=0.0,
                                b3=0.0, b4=0.0))
        assert len(o["anomalie"]) == 2
        assert any("senza distribuzione" in a for a in o["anomalie"])

    def test_voce_degeneri(self):
        for bad in ("x", None, 5, [1]):
            with pytest.raises(ValueError):
                _F["mh551_voce"](bad)
        for bad in (None, "x"):
            with pytest.raises(ValueError):
                _F["mh551_voce"](_v(rl=bad))
        with pytest.raises(ValueError):
            _F["mh551_voce"](_v(b1=math.nan))


class TestW551Demo:
    def test_demo_struttura(self):
        demo = _F["mh551_demo"]()
        assert len(demo) == 4
        assert {d["id"] for d in demo} == {"BOND-IT-001", "BANK-DE-002",
                                          "MARG-UK-003", "LEASE-IT-004"}
        for d in demo:
            assert _F["mh551_voce"](d)["anomalie"] == []

    def test_demo_verdetto(self):
        ri = _F["mh551_riepilogo"](_F["mh551_demo"](), 0.60, 0.40)
        assert ri["verdetto"] == "SCADENZE_BILANCIATE"
        assert ri["importo_tot"] == pytest.approx(281300000.0)
        assert ri["quota_breve"] == pytest.approx(23100000.0 / 281300000.0)
        assert ri["n_anomalie"] == 0


class TestW551Riepilogo:
    def test_nessuna_passivita(self):
        ri = _F["mh551_riepilogo"]([_v(vc=0.0, imp=0.0, b1=0.0, b2=0.0,
                                        b3=0.0, b4=0.0)])
        assert ri["verdetto"] == "NESSUNA_PASSIVITA"

    def test_anomalie(self):
        ri = _F["mh551_riepilogo"]([_v(imp=1000000.0, b1=500000.0,
                                        b2=0.0, b3=0.0, b4=0.0)])
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert ri["n_anomalie"] == 1

    def test_liquidita_tesa(self):
        ri = _F["mh551_riepilogo"]([_v(imp=1000000.0, b1=700000.0,
                                        b2=100000.0, b3=100000.0,
                                        b4=100000.0)], 0.60, 0.40)
        assert ri["verdetto"] == "LIQUIDITA_TESA"

    def test_liquidita_da_monitorare(self):
        ri = _F["mh551_riepilogo"]([_v(imp=1000000.0, b1=450000.0,
                                        b2=200000.0, b3=200000.0,
                                        b4=150000.0)], 0.60, 0.40)
        assert ri["verdetto"] == "LIQUIDITA_DA_MONITORARE"

    def test_per_fascia_e_categoria(self):
        demo = _F["mh551_demo"]()
        ri = _F["mh551_riepilogo"](demo)
        assert ri["per_fascia"]["ENTRO_1_ANNO"] == pytest.approx(23100000.0)
        assert ri["per_fascia"]["OLTRE_5_ANNI"] == pytest.approx(123500000.0)
        assert ri["per_categoria"]["OBBLIGAZIONI_BOND"]["n"] == 1
        assert ri["per_categoria"]["DERIVATI_PASSIVI"]["entro_12m"] == \
            pytest.approx(4200000.0)

    def test_soglie_custom(self):
        ri = _F["mh551_riepilogo"]([_v(vc=1000000.0, imp=1000000.0,
                                        b1=550000.0, b2=150000.0,
                                        b3=150000.0, b4=150000.0)],
                                   0.50, 0.30)
        assert ri["verdetto"] == "LIQUIDITA_TESA"
        ri2 = _F["mh551_riepilogo"]([_v(vc=1000000.0, imp=1000000.0,
                                         b1=550000.0, b2=150000.0,
                                         b3=150000.0, b4=150000.0)],
                                    0.90, 0.40)
        assert ri2["verdetto"] == "LIQUIDITA_DA_MONITORARE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh551_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh551_riepilogo"]("non lista")
        with pytest.raises(ValueError):
            _F["mh551_riepilogo"]([_v()], 0.40, 0.60)
        for bad in (0, 1, -0.1, 1.5, math.nan, math.inf, True, "x",
                    None):
            with pytest.raises(ValueError):
                _F["mh551_riepilogo"]([_v()], bad, 0.40)


class TestW551Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_titolo_551_presente(self):
        assert self._src().count(TITLE551) == 3

    def test_counts_551(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 765
        assert TITLE551 in titoli

    def test_ui_indentata(self):
        assert "    with tab551:" in self._src()

    def test_dvar_line(self):
        assert "tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765 = st.tabs([" in self._src()

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st551_" in ln]
        # le f-string st551_id_{_i551} generano istanze a runtime: la base
        # e' fino al suffisso numerico; csv1/csv2 sono chiavi distinte;
        # la chiave delle 4 fasce e' dinamica (st551_{_k551}_{_i551})
        basi = []
        for ln in righe:
            if "{_k551}" in ln:
                basi += ["st551_b1", "st551_b2", "st551_b3", "st551_b4"]
            else:
                basi.append(re.search(r"st551_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
