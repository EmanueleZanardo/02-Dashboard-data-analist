"""Test tab503 '📦 Cost-of-carry: scomponi il premio del forward': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh503_num", "mh503_str", "mh503_ge0", "mh503_pos", "mh503_pct",
           "mh503_contratto", "mh503_carry", "mh503_riepilogo")

TITLE503 = "📦 Cost-of-carry: scomponi il premio del forward"
TITLE502 = "⚖️ Ribilanciamento: aggiustare l'hedge ratio senza de-designare"

R_TTF = 3.0   # tasso %
U_GAS = 6.0   # stoccaggio %


def _ct(nome, spot, fwd, giorni):
    return _F["mh503_contratto"](nome, spot, fwd, giorni)


def _cy(nome, spot, fwd, giorni, r=R_TTF, u=U_GAS, stocc=True):
    return _F["mh503_carry"](_ct(nome, spot, fwd, giorni), r, u, stocc)


# Demo: un verdetto per tipo (stessi valori della UI)
D_EQ = _ct("TTF Q1-27 (gas)", 39.0, 40.0, 120.0)
D_BW = _ct("Power Cal-27 DE", 88.0, 81.0, 440.0)
D_AN = _ct("PSV baseload IT", 39.2, 42.5, 60.0)


class TestW503Validatori:
    def test_num_ok(self):
        assert _F["mh503_num"](3, "x") == 3.0
        assert _F["mh503_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh503_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh503_str"]("  TTF  ", "x") == "TTF"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh503_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh503_ge0"](0, "x") == 0.0
        assert _F["mh503_ge0"](12.5, "x") == 12.5

    def test_ge0_ko(self):
        with pytest.raises(ValueError):
            _F["mh503_ge0"](-0.01, "x")

    def test_pos_ok(self):
        assert _F["mh503_pos"](0.01, "x") == 0.01
        assert _F["mh503_pos"](100, "x") == 100.0

    def test_pos_ko(self):
        for bad in (0, -1.0, "5"):
            with pytest.raises(ValueError):
                _F["mh503_pos"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh503_pct"](0, "x") == 0.0
        assert _F["mh503_pct"](100, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, float("nan")):
            with pytest.raises(ValueError):
                _F["mh503_pct"](bad, "x")


class TestW503Contratto:
    def test_ok(self):
        c = _ct("TTF", 39.0, 40.0, 120.0)
        assert c == {"nome": "TTF", "spot": 39.0, "fwd": 40.0, "giorni": 120.0}

    def test_ko(self):
        with pytest.raises(ValueError):
            _ct("TTF", 0.0, 40.0, 120.0)     # spot nullo
        with pytest.raises(ValueError):
            _ct("TTF", -5.0, 40.0, 120.0)    # spot negativo
        with pytest.raises(ValueError):
            _ct("TTF", 39.0, -1.0, 120.0)    # forward negativo
        with pytest.raises(ValueError):
            _ct("TTF", 39.0, 40.0, 0.0)       # scadenza nulla
        with pytest.raises(ValueError):
            _ct("  ", 39.0, 40.0, 120.0)     # nome vuoto


class TestW503Carry:
    def test_contango_equo(self):
        v = _cy("TTF Q1-27 (gas)", 39.0, 40.0, 120.0)
        assert v["verdetto"] == "CONTANGO_EQUO"
        # carry = ln(40/39)/(120/365) ~= 7.7%
        assert v["carry_netto_annuo"] == pytest.approx(math.log(40.0 / 39.0) / (120.0 / 365.0))
        # r+u = ln(1.03)+0.06 ~= 8.96% > carry -> y > 0
        assert v["convenience_yield"] > 0.0

    def test_backwardation(self):
        v = _cy("Power Cal-27 DE", 88.0, 81.0, 440.0, stocc=False)
        assert v["verdetto"] == "BACKWARDATION"
        assert v["carry_netto_annuo"] < 0.0
        assert v["premio_eur_mwh"] == pytest.approx(-7.0)

    def test_contango_anomalo(self):
        v = _cy("PSV baseload IT", 39.2, 42.5, 60.0)
        assert v["verdetto"] == "CONTANGO_ANOMALO"
        assert v["convenience_yield"] < 0.0  # y negativa = anomalia

    def test_bordo_carry_zero(self):
        v = _cy("X", 40.0, 40.0, 120.0)  # F == S -> c = 0 -> non < -EPS
        assert v["verdetto"] == "CONTANGO_EQUO"
        assert v["carry_netto_annuo"] == pytest.approx(0.0)

    def test_bordo_r_piu_u(self):
        # F = S*e^((r+u)*T) esatto -> residuo nullo, c == r+u -> EQUO
        r_c = math.log1p(R_TTF / 100.0)
        T = 120.0 / 365.0
        f = 39.0 * math.exp((r_c + U_GAS / 100.0) * T)
        v = _cy("X", 39.0, f, 120.0)
        assert v["verdetto"] == "CONTANGO_EQUO"
        assert v["comp_convenience_eur_mwh"] == pytest.approx(0.0, abs=1e-9)

    def test_componenti_sommano_premio(self):
        v = _cy("TTF Q1-27 (gas)", 39.0, 40.0, 120.0)
        somma = (v["comp_tasso_eur_mwh"] + v["comp_stoccaggio_eur_mwh"]
                 + v["comp_convenience_eur_mwh"])
        assert somma == pytest.approx(v["premio_eur_mwh"], rel=1e-9)

    def test_power_stoccaggio_forzato_zero(self):
        v = _cy("Power Cal-27 DE", 88.0, 81.0, 440.0, u=U_GAS, stocc=False)
        assert v["comp_stoccaggio_eur_mwh"] == pytest.approx(0.0)
        # con u=0 il teorico usa solo r
        T = 440.0 / 365.0
        r_c = math.log1p(R_TTF / 100.0)
        assert v["f_teorico"] == pytest.approx(88.0 * math.exp(r_c * T))

    def test_carry_ko(self):
        with pytest.raises(ValueError):
            _F["mh503_carry"](D_EQ, -1.0, U_GAS, True)   # tasso negativo
        with pytest.raises(ValueError):
            _F["mh503_carry"](D_EQ, R_TTF, -0.5, True)   # stoccaggio negativo
        with pytest.raises(ValueError):
            _F["mh503_carry"](D_EQ, R_TTF, U_GAS, "si")  # stoccabile non bool


class TestW503Riepilogo:
    def _rie(self):
        contratti = [D_EQ, D_BW, _ct("CO2 Dec-26 EUA", 74.0, 75.8, 410.0),
                     D_AN, _ct("TTF Wk-52 (gas)", 38.0, 36.5, 20.0)]
        stocc = [True, False, False, True, True]
        return _F["mh503_riepilogo"](contratti, R_TTF, U_GAS, stocc)

    def test_conteggi_e_complessivo(self):
        rie = self._rie()
        assert rie["n_contratti"] == 5
        assert rie["conteggi"] == {"BACKWARDATION": 2, "CONTANGO_EQUO": 2,
                                   "CONTANGO_ANOMALO": 1}
        assert rie["verdetto_complessivo"] == "CONTANGO_ANOMALO"

    def test_severita_backwardation_sopra_equo(self):
        rie = _F["mh503_riepilogo"]([D_EQ, D_BW], R_TTF, U_GAS, [True, False])
        assert rie["verdetto_complessivo"] == "BACKWARDATION"

    def test_tutti_equi(self):
        rie = _F["mh503_riepilogo"]([D_EQ], R_TTF, U_GAS, [True])
        assert rie["verdetto_complessivo"] == "CONTANGO_EQUO"

    def test_y_media_e_residuo(self):
        rie = self._rie()
        ys = [r["convenience_yield"] for r in rie["righe"]]
        assert rie["convenience_yield_media"] == pytest.approx(sum(ys) / len(ys))
        assert rie["max_residuo_eur_mwh"] == pytest.approx(
            max(abs(r["comp_convenience_eur_mwh"]) for r in rie["righe"]))

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh503_riepilogo"]([], R_TTF, U_GAS, [])
        with pytest.raises(ValueError):
            _F["mh503_riepilogo"]([D_EQ], R_TTF, U_GAS, [True, False])


def test_registry_tab503():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 683
    assert TITLE503 in titoli
    assert src.count(TITLE503) == 3
    assert "tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683 = st.tabs([" in src
    assert "    with tab503:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab503" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab503" in withs
    assert len(withs) == len(dvars) == 683
    # ordine: tab503 dopo tab502
    _decl503 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl503.index(f'"{TITLE502}"') < _decl503.index(f'"{TITLE503}"')
    assert titoli[dvars.index("tab503")] == TITLE503


def test_chiavi_st503_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st503_[^"]+)"', src) + re.findall(
        r'key=f"(st503_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
