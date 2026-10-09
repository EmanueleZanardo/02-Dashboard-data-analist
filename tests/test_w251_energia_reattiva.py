"""Test tab251 'Energia reattiva & penali cosphi': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab251.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("r251_fattore_potenza", "r251_eccedenze", "r251_penale",
          "r251_rifasamento", "r251_payback", "r251_analisi_fasce")
r251_fattore_potenza = _F["r251_fattore_potenza"]
r251_eccedenze = _F["r251_eccedenze"]
r251_penale = _F["r251_penale"]
r251_rifasamento = _F["r251_rifasamento"]
r251_payback = _F["r251_payback"]
r251_analisi_fasce = _F["r251_analisi_fasce"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab251:
    def test_tab251_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 323
        assert "⚡ Energia reattiva & penali cosφ" in titoli
        assert "tab251" in dvars
        assert "tab251" in withs
        assert titoli[dvars.index("tab251")] == "⚡ Energia reattiva & penali cosφ"
        assert titoli[-1] == "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
        keys = re.findall(r'key="(r251_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_250_251(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab250")] == "💸 Capitale circolante"
        assert titoli[dvars.index("tab251")] == "⚡ Energia reattiva & penali cosφ"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("r251_fattore_potenza", "r251_eccedenze", "r251_penale",
                   "r251_rifasamento", "r251_payback", "r251_analisi_fasce"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestR251FattorePotenza:
    def test_base(self):
        # tan = 400/1000 = 0.4, cos = 1/sqrt(1.16) = 0.9285
        r = r251_fattore_potenza(1000, 400)
        assert r["tan_phi"] == pytest.approx(0.4, abs=1e-4)
        assert r["cos_phi"] == pytest.approx(0.9285, abs=1e-4)

    def test_reattiva_nulla(self):
        r = r251_fattore_potenza(1000, 0)
        assert r["tan_phi"] == 0.0
        assert r["cos_phi"] == 1.0

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_fattore_potenza(0, 400)
        with pytest.raises(ValueError):
            r251_fattore_potenza(-100, 400)
        with pytest.raises(ValueError):
            r251_fattore_potenza(1000, -50)
        with pytest.raises(ValueError):
            r251_fattore_potenza(float("nan"), 400)


class TestR251Eccedenze:
    def test_solo_fascia1(self):
        # P=1000: lim1=330, lim2=750; Q=400 -> f1=70, f2=0, esente=330
        r = r251_eccedenze(1000, 400)
        assert r == {"attiva_kwh": 1000.0, "reattiva_kvarh": 400.0,
                     "q_esente_kvarh": 330.0, "q_fascia1_kvarh": 70.0,
                     "q_fascia2_kvarh": 0.0}

    def test_entrambe_le_fasce(self):
        # Q=900 -> f1=750-330=420, f2=900-750=150, esente=330
        r = r251_eccedenze(1000, 900)
        assert r["q_fascia1_kvarh"] == 420.0
        assert r["q_fascia2_kvarh"] == 150.0
        assert r["q_esente_kvarh"] == 330.0

    def test_sotto_soglia(self):
        r = r251_eccedenze(1000, 200)
        assert r["q_fascia1_kvarh"] == 0.0
        assert r["q_fascia2_kvarh"] == 0.0
        assert r["q_esente_kvarh"] == 200.0

    def test_soglie_custom(self):
        # soglie 50/100: P=1000 -> lim1=500, lim2=1000; Q=800 -> f1=300
        r = r251_eccedenze(1000, 800, 50.0, 100.0)
        assert r["q_fascia1_kvarh"] == 300.0
        assert r["q_fascia2_kvarh"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_eccedenze(0, 400)
        with pytest.raises(ValueError):
            r251_eccedenze(1000, -10)
        with pytest.raises(ValueError):
            r251_eccedenze(1000, 400, 75.0, 33.0)  # s1 > s2
        with pytest.raises(ValueError):
            r251_eccedenze(1000, 400, 0.0, 75.0)  # s1 <= 0
        with pytest.raises(ValueError):
            r251_eccedenze(1000, float("nan"))


class TestR251Penale:
    def test_base(self):
        ecc = {"q_esente_kvarh": 330.0, "q_fascia1_kvarh": 420.0,
               "q_fascia2_kvarh": 150.0}
        r = r251_penale(ecc, 0.046, 0.061)
        # 420*0.046=19.32, 150*0.061=9.15, tot=28.47
        assert r["penale_fascia1_eur"] == pytest.approx(19.32, abs=0.01)
        assert r["penale_fascia2_eur"] == pytest.approx(9.15, abs=0.01)
        assert r["penale_totale_eur"] == pytest.approx(28.47, abs=0.01)

    def test_zero(self):
        ecc = {"q_esente_kvarh": 330.0, "q_fascia1_kvarh": 0.0,
               "q_fascia2_kvarh": 0.0}
        r = r251_penale(ecc, 0.046, 0.061)
        assert r["penale_totale_eur"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_penale("nonsense", 0.046, 0.061)
        with pytest.raises(ValueError):
            r251_penale({"q_fascia1_kvarh": 1.0}, 0.046, 0.061)
        with pytest.raises(ValueError):
            r251_penale({"q_fascia1_kvarh": 1.0, "q_fascia2_kvarh": 0.0},
                        -0.01, 0.061)


class TestR251Rifasamento:
    def test_base(self):
        # P=1000kWh, Q=400kVArh, 730h -> P_med=1.3699kW, tan=0.4
        # tan(acos 0.95)=0.32868 -> Qc=1.3699*(0.4-0.32868)=0.0977 -> 0.10
        r = r251_rifasamento(1000, 400, 0.95, 730.0)
        assert r["potenza_media_kw"] == pytest.approx(1.37, abs=0.01)
        assert r["reattiva_media_kvar"] == pytest.approx(0.55, abs=0.01)
        assert r["batteria_kvar"] == pytest.approx(0.10, abs=0.005)

    def test_gia_in_regola(self):
        # tan=0.2 < tan_target -> batteria 0
        r = r251_rifasamento(1000, 200, 0.95, 730.0)
        assert r["batteria_kvar"] == 0.0

    def test_target_piu_spinto_piu_kvar(self):
        b95 = r251_rifasamento(1000, 400, 0.95, 730.0)["batteria_kvar"]
        b99 = r251_rifasamento(1000, 400, 0.99, 730.0)["batteria_kvar"]
        assert b99 > b95 > 0

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_rifasamento(1000, 400, 1.0, 730.0)
        with pytest.raises(ValueError):
            r251_rifasamento(1000, 400, 0.0, 730.0)
        with pytest.raises(ValueError):
            r251_rifasamento(1000, 400, 0.95, 0.0)
        with pytest.raises(ValueError):
            r251_rifasamento(0, 400, 0.95, 730.0)


class TestR251Payback:
    def test_base(self):
        # invest=23.65*25=591.25; mesi=591.25/9439.2*12=0.75 -> 0.8
        r = r251_payback(9439.2, 23.65, 25.0)
        assert r["investimento_eur"] == pytest.approx(591.25, abs=0.01)
        assert r["payback_mesi"] == pytest.approx(0.8, abs=0.05)
        assert r["conviene"] is True

    def test_non_conviene(self):
        r = r251_payback(100.0, 1000.0, 25.0)  # 25000/100*12=3000 mesi
        assert r["conviene"] is False
        assert r["payback_mesi"] == pytest.approx(3000.0, abs=1.0)

    def test_nessuna_penale(self):
        r = r251_payback(0.0, 10.0, 25.0)
        assert r["payback_mesi"] is None
        assert r["conviene"] is False

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_payback(-100.0, 10.0, 25.0)
        with pytest.raises(ValueError):
            r251_payback(100.0, -5.0, 25.0)


class TestR251AnalisiFasce:
    def test_due_fasce(self):
        righe = r251_analisi_fasce([1000.0, 2000.0], [400.0, 1800.0],
                                   ["F1", "F2"], 0.046, 0.061)
        assert len(righe) == 2
        f1, f2 = righe
        assert f1["fascia"] == "F1"
        assert f1["penale_eur"] == pytest.approx(70 * 0.046, abs=0.01)
        # F2: P=2000 lim1=660 lim2=1500; Q=1800 -> f1=840, f2=300
        assert f2["q_fascia1_kvarh"] == 840.0
        assert f2["q_fascia2_kvarh"] == 300.0
        assert f2["penale_eur"] == pytest.approx(840 * 0.046 + 300 * 0.061,
                                                abs=0.01)
        assert f2["cos_phi"] == pytest.approx(1 / math.sqrt(1 + 0.9 ** 2),
                                              abs=1e-4)

    def test_errori(self):
        with pytest.raises(ValueError):
            r251_analisi_fasce([1000.0], [400.0, 500.0], ["F1", "F2"],
                               0.046, 0.061)
        with pytest.raises(ValueError):
            r251_analisi_fasce([], [], [], 0.046, 0.061)
