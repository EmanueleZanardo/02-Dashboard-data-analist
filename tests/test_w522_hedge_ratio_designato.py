"""Test tab522 '⚖️📋 Hedge ratio designato (IFRS 9 6.4.1(c)(iii))': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh522_num", "mh522_str", "mh522_relazione", "mh522_verifica",
           "mh522_riepilogo")

TITLE522 = "⚖️📋 Hedge ratio designato (IFRS 9 6.4.1(c)(iii))"
TITLE521 = "🧱 Basis adjustment (adeguamento del costo, IFRS 9 6.5.11)"


def _r(rid="HEDGE-2026-001", qi=10000.0, qs=8000.0, he=0.80,
       dfv=-150000.0, d="Acquisto forecast power"):
    return {"id": rid, "qta_item": qi, "qta_strumento": qs,
            "hr_effettivo": he, "delta_fv_item": dfv, "descrizione": d}


class TestW522Validatori:
    def test_num_ok(self):
        assert _F["mh522_num"](2, "x") == 2.0
        assert _F["mh522_num"](-12000.5, "x") == -12000.5
        assert _F["mh522_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh522_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh522_str"]("  HEDGE-1 ", "x") == "HEDGE-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh522_str"](bad, "x")


class TestW522Relazione:
    def test_ok(self):
        r = _F["mh522_relazione"](_r())
        assert r["id"] == "HEDGE-2026-001"
        assert r["qta_item"] == pytest.approx(10000.0)
        assert r["qta_strumento"] == pytest.approx(8000.0)
        assert r["hr_effettivo"] == pytest.approx(0.80)
        assert r["delta_fv_item"] == pytest.approx(-150000.0)
        assert r["descrizione"] == "Acquisto forecast power"

    def test_dfv_default_e_descrizione_default(self):
        d = _r()
        del d["delta_fv_item"]
        del d["descrizione"]
        r = _F["mh522_relazione"](d)
        assert r["delta_fv_item"] == 0.0
        assert r["descrizione"] == ""

    def test_quantita_ko(self):
        for bad in (0, -5, True, float("nan"), "100"):
            with pytest.raises(ValueError):
                _F["mh522_relazione"](_r(qi=bad))
        for bad in (0, -5, float("inf")):
            with pytest.raises(ValueError):
                _F["mh522_relazione"](_r(qs=bad))

    def test_hr_effettivo_ko(self):
        for bad in (0, -0.8, True, float("nan"), "0.8"):
            with pytest.raises(ValueError):
                _F["mh522_relazione"](_r(he=bad))

    def test_chiave_mancante(self):
        d = _r()
        del d["hr_effettivo"]
        with pytest.raises(ValueError):
            _F["mh522_relazione"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh522_relazione"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh522_relazione"](_r(rid="  "))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh522_relazione"](_r(d=5))


class TestW522Verifica:
    def test_demo_allineato(self):
        r = _F["mh522_verifica"](_r())
        assert r["hr_designato"] == pytest.approx(0.80)
        assert r["hr_effettivo"] == pytest.approx(0.80)
        assert r["squilibrio"] == pytest.approx(0.0)
        assert r["esito"] == "ALLINEATO"
        assert r["motivo"] == ""
        assert r["inefficacia_attesa"] == 0.0
        assert r["copertura_item_pct"] == pytest.approx(80.0)

    def test_squilibrio_oltre_soglia(self):
        r = _F["mh522_verifica"](_r(rid="HEDGE-2026-002", qs=5000.0))
        assert r["hr_designato"] == pytest.approx(0.50)
        assert r["squilibrio"] == pytest.approx(-0.30)
        assert r["esito"] == "SQUILIBRIO_OLTRE_SOGLIA"
        assert "5.00%" in r["motivo"]
        # 0.30 x 150'000 = 45'000
        assert r["inefficacia_attesa"] == pytest.approx(45000.0)
        assert r["copertura_item_pct"] == pytest.approx(50.0)

    def test_squilibrio_entro_soglia(self):
        r = _F["mh522_verifica"](_r(rid="E", qs=8300.0))
        assert r["hr_designato"] == pytest.approx(0.83)
        assert r["esito"] == "SQUILIBRIO_ENTRO_SOGLIA"
        assert "tolleranza" in r["motivo"]
        assert r["inefficacia_attesa"] == pytest.approx(
            0.03 * 150000.0)

    def test_epsilon_tolleranza(self):
        # squilibrio esattamente alla tolleranza -> ALLINEATO
        r = _F["mh522_verifica"](_r(rid="E", qs=8100.0),
                                 tolleranza=0.01, soglia=0.05)
        assert r["esito"] == "ALLINEATO"

    def test_epsilon_soglia(self):
        # squilibrio esattamente alla soglia -> ENTRO_SOGLIA
        r = _F["mh522_verifica"](_r(rid="E", qs=8500.0),
                                 tolleranza=0.01, soglia=0.05)
        assert r["esito"] == "SQUILIBRIO_ENTRO_SOGLIA"

    def test_tolleranza_custom(self):
        r = _F["mh522_verifica"](_r(rid="E", qs=8300.0),
                                 tolleranza=0.05, soglia=0.10)
        assert r["esito"] == "ALLINEATO"

    def test_dfv_positivo_e_zero(self):
        r = _F["mh522_verifica"](_r(rid="P", qs=5000.0, dfv=200000.0))
        assert r["inefficacia_attesa"] == pytest.approx(60000.0)
        r0 = _F["mh522_verifica"](_r(rid="Z", qs=5000.0, dfv=0.0))
        assert r0["inefficacia_attesa"] == 0.0

    def test_sovracopertura(self):
        # designato > gestionale: squilibrio positivo
        r = _F["mh522_verifica"](_r(rid="S", qi=10000.0, qs=12000.0,
                                    he=0.80))
        assert r["hr_designato"] == pytest.approx(1.20)
        assert r["squilibrio"] == pytest.approx(0.40)
        assert r["esito"] == "SQUILIBRIO_OLTRE_SOGLIA"

    def test_soglie_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh522_verifica"](_r(), tolleranza=-0.01)
        with pytest.raises(ValueError):
            _F["mh522_verifica"](_r(), soglia=0.0)
        with pytest.raises(ValueError):
            _F["mh522_verifica"](_r(), tolleranza=0.05, soglia=0.05)
        with pytest.raises(ValueError):
            _F["mh522_verifica"](_r(), tolleranza=float("nan"))

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh522_verifica"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh522_verifica"]({"id": "X"})


class TestW522Riepilogo:
    def test_misto(self):
        a = _F["mh522_riepilogo"](
            [_r(), _r(rid="HEDGE-2026-002", qs=5000.0,
                      d="Swap dimezzato")])
        t = a["totali"]
        assert t["n_relazioni"] == 2
        assert t["n_allineate"] == 1
        assert t["n_non_allineate"] == 1
        assert t["n_oltre_soglia"] == 1
        assert t["totale_inefficacia_attesa"] == pytest.approx(45000.0)
        assert t["hr_designato_medio"] == pytest.approx(0.65)
        assert t["verdetto_complessivo"] == "MISTO"

    def test_tutti_allineati(self):
        a = _F["mh522_riepilogo"]([_r(), _r(rid="H2", qs=8100.0)])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "TUTTI_ALLINEATI"
        # H2: |0.81-0.80| = 0.01 (alla tolleranza, ALLINEATO) ma con
        # inefficacia residua 0.01 x 150'000
        assert t["totale_inefficacia_attesa"] == pytest.approx(1500.0)

    def test_nessuno_allineato(self):
        a = _F["mh522_riepilogo"](
            [_r(rid="A", qs=5000.0), _r(rid="B", qs=3000.0)])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "NESSUNO_ALLINEATO"
        assert t["n_allineate"] == 0
        assert t["n_oltre_soglia"] == 2
        assert t["totale_inefficacia_attesa"] == pytest.approx(
            0.30 * 150000.0 + 0.50 * 150000.0)

    def test_wrapper_parita_verifica(self):
        a = _F["mh522_riepilogo"]([_r()])
        v = _F["mh522_verifica"](_r())
        assert a["righe"][0]["hr_designato"] == pytest.approx(
            v["hr_designato"])
        assert a["righe"][0]["esito"] == v["esito"]

    def test_tolleranza_passata_al_wrapper(self):
        a = _F["mh522_riepilogo"]([_r(rid="E", qs=8300.0)],
                                  tolleranza=0.05, soglia=0.10)
        assert a["righe"][0]["esito"] == "ALLINEATO"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh522_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh522_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh522_riepilogo"]([_r(rid="A"), _r(rid="A")])


def test_registry_tab522():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 775
    assert TITLE522 in titoli
    assert TITLE521 in titoli
    assert src.count(TITLE522) == 3
    assert ", tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775 = st.tabs([" in src
