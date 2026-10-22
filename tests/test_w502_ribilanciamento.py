"""Test tab502 '⚖️ Ribilanciamento: aggiustare l'hedge ratio senza de-designare': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh502_num", "mh502_str", "mh502_ge0", "mh502_pos", "mh502_pct",
           "mh502_relazione", "mh502_verdetto", "mh502_riepilogo")

TITLE502 = "⚖️ Ribilanciamento: aggiustare l'hedge ratio senza de-designare"
TITLE501 = "🛑 De-designazione: continuare o chiudere la copertura?"

TGT, TOL, SPR, BUD, LOT = 1.0, 5.0, 0.50, 5000.0, 500.0


def _rel(nome, esp, q):
    return _F["mh502_relazione"](nome, esp, q)


def _verd(riga, target=TGT, tol=TOL, spr=SPR, bud=BUD, lot=LOT):
    v = _F["mh502_verdetto"](riga, target, tol, spr, bud, lot)
    return v["verdetto"], v


# Demo: uno per ogni verdetto (ordine delle regole: la prima che scatta vince)
R_MAN = _rel("TTF Q1-27 future", 10000.0, 9800.0)   # ratio 0.98 -> MANTIENI
R_RIB = _rel("Power Cal-27 DE", 6000.0, 4500.0)      # delta 1500, costo 750 -> RIBILANCIA
R_VEN = _rel("CO2 Dec-26 EUA", 5000.0, 6400.0)       # delta -1400 -> RIBILANCIA (vendi)
R_LOT = _rel("PSV baseload IT", 2000.0, 1880.0)      # ratio 0.94, delta 120 < 500 -> LOTTO_MINIMO
R_COS = _rel("Gas spot proxy", 50000.0, 20000.0)     # delta 30000, costo 15000 -> COSTO_ECCESSIVO


class TestW502Validatori:
    def test_num_ok(self):
        assert _F["mh502_num"](3, "x") == 3.0
        assert _F["mh502_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh502_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh502_str"]("  TTF  ", "x") == "TTF"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh502_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh502_ge0"](0, "x") == 0.0
        assert _F["mh502_ge0"](12.5, "x") == 12.5

    def test_ge0_ko(self):
        with pytest.raises(ValueError):
            _F["mh502_ge0"](-0.01, "x")

    def test_pos_ok(self):
        assert _F["mh502_pos"](0.01, "x") == 0.01
        assert _F["mh502_pos"](100, "x") == 100.0

    def test_pos_ko(self):
        for bad in (0, -1.0, "5"):
            with pytest.raises(ValueError):
                _F["mh502_pos"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh502_pct"](0, "x") == 0.0
        assert _F["mh502_pct"](100, "x") == 100.0
        assert _F["mh502_pct"](5.0, "x") == 5.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, float("nan")):
            with pytest.raises(ValueError):
                _F["mh502_pct"](bad, "x")


class TestW502Relazione:
    def test_ratio(self):
        r = _rel("TTF", 10000.0, 9800.0)
        assert r["ratio"] == pytest.approx(0.98)
        assert r["esp_coperta"] == 10000.0
        assert r["q_strumento"] == 9800.0

    def test_relazione_ko(self):
        with pytest.raises(ValueError):
            _rel("TTF", 0.0, 9800.0)        # esp nulla
        with pytest.raises(ValueError):
            _rel("TTF", -100.0, 9800.0)     # esp negativa
        with pytest.raises(ValueError):
            _rel("TTF", 10000.0, -1.0)      # q negativa
        with pytest.raises(ValueError):
            _rel("  ", 10000.0, 9800.0)     # nome vuoto


class TestW502Verdetto:
    def test_dentro_banda_mantieni(self):
        ve, v = _verd(R_MAN)
        assert ve == "MANTIENI"
        assert v["delta_q_mwh"] == pytest.approx(200.0)

    def test_bordo_banda_incluso(self):
        r = _rel("X", 10000.0, 9500.0)  # ratio 0.95, banda ±5% -> limite incluso
        ve, _ = _verd(r)
        assert ve == "MANTIENI"

    def test_fuori_banda_ribilancia_compra(self):
        ve, v = _verd(R_RIB)
        assert ve == "RIBILANCIA"
        assert v["delta_q_mwh"] == pytest.approx(1500.0)
        assert v["costo_eur"] == pytest.approx(750.0)
        assert v["verso"] == "compra"

    def test_fuori_banda_ribilancia_vendi(self):
        ve, v = _verd(R_VEN)
        assert ve == "RIBILANCIA"
        assert v["delta_q_mwh"] == pytest.approx(-1400.0)
        assert v["costo_eur"] == pytest.approx(700.0)
        assert v["verso"] == "vendi"

    def test_delta_sotto_lotto(self):
        ve, v = _verd(R_LOT)
        assert ve == "LOTTO_MINIMO"
        assert v["delta_q_mwh"] == pytest.approx(120.0)
        assert v["verso"] == "compra"

    def test_delta_pari_al_lotto_ribilancia(self):
        r = _rel("X", 10000.0, 9500.0)  # delta 500 = lotto -> regola 2 non scatta
        ve, _ = _verd(r, tol=0.0)
        assert ve == "RIBILANCIA"

    def test_costo_oltre_budget(self):
        ve, v = _verd(R_COS)
        assert ve == "COSTO_ECCESSIVO"
        assert v["costo_eur"] == pytest.approx(15000.0)

    def test_costo_pari_al_budget_ribilancia(self):
        r = _rel("X", 20000.0, 10000.0)  # delta 10000, costo 5000 = budget
        ve, _ = _verd(r, tol=0.0)
        assert ve == "RIBILANCIA"

    def test_ordine_regole_banda_vince_su_lotto(self):
        # ratio 0.96 dentro banda ±5%: MANTIENI anche con delta 400 < lotto
        r = _rel("X", 10000.0, 9600.0)
        ve, _ = _verd(r)
        assert ve == "MANTIENI"

    def test_ordine_regole_lotto_vince_su_costo(self):
        # delta 400 < lotto 500 e costo 2000 > budget 1000: regola 2 prima della 3
        r = _rel("X", 10000.0, 9600.0)
        ve, _ = _verd(r, tol=0.0, spr=5.0, bud=1000.0)
        assert ve == "LOTTO_MINIMO"

    def test_target_diverso_da_uno(self):
        r = _rel("X", 10000.0, 7800.0)  # ratio 0.78, target 0.8 ±5% -> dentro
        ve, _ = _verd(r, target=0.8)
        assert ve == "MANTIENI"
        r2 = _rel("X", 10000.0, 7000.0)  # ratio 0.7: delta 1000 -> RIBILANCIA
        ve2, _ = _verd(r2, target=0.8)
        assert ve2 == "RIBILANCIA"

    def test_verdetto_ko(self):
        with pytest.raises(ValueError):
            _F["mh502_verdetto"](R_MAN, 0.0, TOL, SPR, BUD, LOT)     # target 0
        with pytest.raises(ValueError):
            _F["mh502_verdetto"](R_MAN, TGT, 150.0, SPR, BUD, LOT)   # tol > 100
        with pytest.raises(ValueError):
            _F["mh502_verdetto"](R_MAN, TGT, TOL, -0.1, BUD, LOT)    # spread < 0


class TestW502Riepilogo:
    def test_riepilogo_conteggi(self):
        rie = _F["mh502_riepilogo"]([R_MAN, R_RIB, R_VEN, R_LOT, R_COS],
                                    TGT, TOL, SPR, BUD, LOT)
        assert rie["n_relazioni"] == 5
        c = rie["conteggi"]
        assert c == {"COSTO_ECCESSIVO": 1, "LOTTO_MINIMO": 1,
                     "RIBILANCIA": 2, "MANTIENI": 1}
        assert [r["verdetto"] for r in rie["righe"]] == [
            "MANTIENI", "RIBILANCIA", "RIBILANCIA", "LOTTO_MINIMO",
            "COSTO_ECCESSIVO"]

    def test_riepilogo_volume_e_costo(self):
        # solo le righe RIBILANCIA contano in volume e costo
        rie = _F["mh502_riepilogo"]([R_MAN, R_RIB, R_VEN, R_LOT, R_COS],
                                    TGT, TOL, SPR, BUD, LOT)
        assert rie["volume_da_scambiare_mwh"] == pytest.approx(2900.0)
        assert rie["costo_ribilanciamento_totale_eur"] == pytest.approx(1450.0)

    def test_riepilogo_complessivo_il_piu_severo(self):
        rie = _F["mh502_riepilogo"]([R_MAN, R_RIB, R_VEN, R_LOT, R_COS],
                                    TGT, TOL, SPR, BUD, LOT)
        assert rie["verdetto_complessivo"] == "COSTO_ECCESSIVO"
        rie2 = _F["mh502_riepilogo"]([R_MAN, R_RIB], TGT, TOL, SPR, BUD, LOT)
        assert rie2["verdetto_complessivo"] == "RIBILANCIA"
        rie3 = _F["mh502_riepilogo"]([R_MAN, R_LOT], TGT, TOL, SPR, BUD, LOT)
        assert rie3["verdetto_complessivo"] == "LOTTO_MINIMO"
        rie4 = _F["mh502_riepilogo"]([R_MAN], TGT, TOL, SPR, BUD, LOT)
        assert rie4["verdetto_complessivo"] == "MANTIENI"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh502_riepilogo"]([], TGT, TOL, SPR, BUD, LOT)
        with pytest.raises(ValueError):
            _F["mh502_riepilogo"]([R_MAN], TGT, TOL, SPR, -1.0, LOT)


def test_registry_tab502():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 628
    assert TITLE502 in titoli
    assert src.count(TITLE502) == 3
    assert "tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628 = st.tabs([" in src
    assert "    with tab502:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab502" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab502" in withs
    assert len(withs) == len(dvars) == 628
    # ordine: tab502 dopo tab501
    _decl502 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl502.index(f'"{TITLE501}"') < _decl502.index(f'"{TITLE502}"')
    assert titoli[dvars.index("tab502")] == TITLE502


def test_chiavi_st502_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st502_[^"]+)"', src) + re.findall(
        r'key=f"(st502_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10
