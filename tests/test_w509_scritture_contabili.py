"""Test tab509 '🧾 Scritture contabili (IFRS 9)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh509_num", "mh509_str", "mh509_data", "mh509_riga",
           "mh509_registrazione", "mh509_scritture", "mh509_mastro",
           "mh509_riepilogo")

TITLE509 = "🧾 Scritture contabili (IFRS 9)"
TITLE508 = "📝 Documentazione della copertura (IFRS 9)"


def _demo():
    return [
        {"periodo": "Q1 2026", "data": "2026-03-31",
         "delta_fv_strumento": 45000.0, "quota_efficace": 44100.0,
         "recycling_oci": 0.0},
        {"periodo": "Q2 2026", "data": "2026-06-30",
         "delta_fv_strumento": -30000.0, "quota_efficace": -29400.0,
         "recycling_oci": 35000.0},
        {"periodo": "Lug 2026", "data": "2026-07-31",
         "delta_fv_strumento": 22000.0, "quota_efficace": 21560.0,
         "recycling_oci": 18000.0},
        {"periodo": "Ago 2026", "data": "2026-08-31",
         "delta_fv_strumento": -14000.0, "quota_efficace": -13720.0,
         "recycling_oci": 15000.0},
    ]


class TestW509Validatori:
    def test_num_ok(self):
        assert _F["mh509_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh509_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh509_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh509_str"](bad, "x")

    def test_data_ok(self):
        assert _F["mh509_data"]("2026-10-16") == "2026-10-16"

    def test_data_ko(self):
        for bad in (None, "", "16/10/2026", "2026-13-01", "2026-02-30"):
            with pytest.raises(ValueError):
                _F["mh509_data"](bad)
        with pytest.raises(ValueError):
            _F["mh509_data"]("2099-01-01")  # futura


class TestW509Riga:
    def test_dare(self):
        r = _F["mh509_riga"]("Riserva OCI - copertura CFH", 100.0, 0.0)
        assert r["dare"] == 100.0 and r["avere"] == 0.0

    def test_avere(self):
        r = _F["mh509_riga"]("Riserva OCI - copertura CFH", 0.0, 250.5)
        assert r["dare"] == 0.0 and r["avere"] == 250.5

    def test_due_lati_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_riga"]("C", 10.0, 10.0)

    def test_nulla_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_riga"]("C", 0.0, 0.0)

    def test_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_riga"]("C", -5.0, 0.0)

    def test_conto_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_riga"]("", 5.0, 0.0)


class TestW509Registrazione:
    def test_quadrata(self):
        r = _F["mh509_registrazione"](
            "2026-03-31", "Copertura CFH HR-1 - Q1",
            [_F["mh509_riga"]("Strumento derivato - FV", 45000.0, 0.0),
             _F["mh509_riga"]("Riserva OCI - copertura CFH", 0.0, 44100.0),
             _F["mh509_riga"]("Utile da inefficacia - P&L", 0.0, 900.0)])
        assert r["quadrata"]
        assert r["totale_dare"] == 45000.0
        assert r["totale_avere"] == 45000.0

    def test_non_quadrata_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_registrazione"](
                "2026-03-31", "C",
                [_F["mh509_riga"]("A", 100.0, 0.0),
                 _F["mh509_riga"]("B", 0.0, 99.0)])

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_registrazione"]("2026-03-31", "C", [])

    def test_data_futura_ko(self):
        with pytest.raises(ValueError):
            _F["mh509_registrazione"](
                "2099-01-01", "C",
                [_F["mh509_riga"]("A", 10.0, 0.0),
                 _F["mh509_riga"]("B", 0.0, 10.0)])


class TestW509Scritture:
    def test_demo_quattro_periodi(self):
        s = _F["mh509_riepilogo"]("HR-2026-001", _demo())
        assert s["n_registrazioni"] == 4
        assert s["tutte_quadrate"]
        assert s["totale_dare"] == pytest.approx(179000.0)
        assert s["totale_avere"] == pytest.approx(179000.0)
        # Q1: D Derivato 45000 (44100 eff + 900 ineff), A Riserva 44100,
        #     A Utile P&L 900
        q1 = s["registrazioni"][0]
        assert q1["totale_dare"] == 45000.0
        assert len(q1["righe"]) == 4
        # Q2: include inefficacia negativa + recycling
        q2 = s["registrazioni"][1]
        assert q2["totale_dare"] == 65000.0
        conti2 = {r["conto"] for r in q2["righe"]}
        assert "Perdita da inefficacia - P&L" in conti2
        assert "Ricavi da recycling - P&L" in conti2

    def test_mastro(self):
        s = _F["mh509_riepilogo"]("HR-2026-001", _demo())
        m = {c["conto"]: c for c in s["mastro"]}
        der = m["Strumento derivato - FV"]
        assert der["dare"] == pytest.approx(67000.0)
        assert der["avere"] == pytest.approx(44000.0)
        assert der["saldo"] == pytest.approx(23000.0)
        oci = m["Riserva OCI - copertura CFH"]
        assert oci["avere"] == pytest.approx(65660.0)
        assert oci["dare"] == pytest.approx(111120.0)
        # saldo mastro coerente con totale dare/avere
        assert sum(c["saldo"] for c in s["mastro"]) == pytest.approx(0.0)

    def test_periodo_senza_movimenti_saltato(self):
        s = _F["mh509_riepilogo"](
            "HR-1",
            [{"periodo": "P1", "data": "2026-01-31",
              "delta_fv_strumento": 0.0, "quota_efficace": 0.0,
              "recycling_oci": 0.0}])
        assert s["n_registrazioni"] == 0
        assert s["totale_dare"] == 0.0
        assert s["tutte_quadrate"]

    def test_recycling_negativo(self):
        s = _F["mh509_riepilogo"](
            "HR-1",
            [{"periodo": "P1", "data": "2026-01-31",
              "delta_fv_strumento": 1000.0, "quota_efficace": 980.0,
              "recycling_oci": -200.0}])
        conti = {r["conto"] for r in s["registrazioni"][0]["righe"]}
        assert "Costi da recycling - P&L" in conti
        assert s["tutte_quadrate"]

    def test_degenere(self):
        # |quota_efficace| > |delta_fv|
        with pytest.raises(ValueError):
            _F["mh509_riepilogo"](
                "HR-1",
                [{"periodo": "P1", "data": "2026-01-31",
                  "delta_fv_strumento": 1000.0, "quota_efficace": 1100.0,
                  "recycling_oci": 0.0}])
        # segni discordi
        with pytest.raises(ValueError):
            _F["mh509_riepilogo"](
                "HR-1",
                [{"periodo": "P1", "data": "2026-01-31",
                  "delta_fv_strumento": 1000.0, "quota_efficace": -900.0,
                  "recycling_oci": 0.0}])
        # chiave mancante
        with pytest.raises(ValueError):
            _F["mh509_riepilogo"](
                "HR-1", [{"periodo": "P1", "data": "2026-01-31"}])
        # relazione vuota
        with pytest.raises(ValueError):
            _F["mh509_riepilogo"]("  ", _demo())
        # data futura
        with pytest.raises(ValueError):
            _F["mh509_riepilogo"](
                "HR-1",
                [{"periodo": "P1", "data": "2099-01-31",
                  "delta_fv_strumento": 1000.0, "quota_efficace": 980.0,
                  "recycling_oci": 0.0}])


def test_registry_tab509():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 818
    assert TITLE509 in titoli
    assert src.count(TITLE509) == 3
    assert ", tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818 = st.tabs([" in src
    assert "    with tab509:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab509" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab509" in withs
    assert len(withs) == len(dvars) == 818
    # ordine: tab509 dopo tab508
    _decl509 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl509.index(f'"{TITLE508}"') < _decl509.index(f'"{TITLE509}"')
    assert titoli[dvars.index("tab509")] == TITLE509


def test_chiavi_st509_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st509_[^"]+)"', src) + re.findall(
        r'key=f"(st509_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
