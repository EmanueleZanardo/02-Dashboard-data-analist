"""Test tab474 '⏰ Frequenza di ribilanciamento': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh474_num", "mh474_frequenza", "mh474_costo_annuo",
           "mh474_verdetto")

TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"

# Demo: stessi numeri tab473 (costo 1000 EUR, fuori budget 67837 EUR,
# deviazione massima B +107.2%), drift 5%/settimana
K, F, G, D = 1000.0, 67837.0, 0.05, 1.072

A_EXP = 1582.0195895522388
TS_EXP = 0.7950493219825565
CS_EXP = 130809.49461180951
N_EXP = 65.40474730590473

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh474_frequenza"](K, F, G, D)
    return _DEMO


class TestRegistry474:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 727
        assert "tab474" in dvars
        assert "tab474" in withs

    def test_titoli_allineati_471_472_473_474(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {471: TITLE471, 472: TITLE472, 473: TITLE473,
                  474: TITLE474}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 4


class TestFrequenza474:
    def test_demo_coerenza(self):
        m = _demo()
        assert m["a_eur_sett2"] == pytest.approx(A_EXP)
        assert m["T_star_sett"] == pytest.approx(TS_EXP)
        assert m["costo_annuo_ottimo"] == pytest.approx(CS_EXP)
        assert m["ribilanciamenti_anno"] == pytest.approx(N_EXP)
        assert m["costo_ribil_ciclo"] == pytest.approx(K)
        assert m["drift_cumulato_ciclo"] == pytest.approx(K)  # 50/50

    def test_ottimo_in_forma_chiusa(self):
        # T* = sqrt(K/a) calcolato a mano, percorso indipendente
        a = F * G / (2.0 * D)
        assert _demo()["T_star_sett"] == pytest.approx(math.sqrt(K / a))

    def test_costo_annuo_coerente(self):
        m = _demo()
        c = _F["mh474_costo_annuo"](m["T_star_sett"], K, m["a_eur_sett2"])
        assert c == pytest.approx(m["costo_annuo_ottimo"])

    def test_minimo_esatto(self):
        # C(T*-h) e C(T*+h) sono entrambi >= C(T*): T* e' il minimo
        m = _demo()
        ts, a = m["T_star_sett"], m["a_eur_sett2"]
        c_star = m["costo_annuo_ottimo"]
        for t in (ts * 0.5, ts * 0.9, ts * 1.1, ts * 2.0):
            assert _F["mh474_costo_annuo"](t, K, a) >= c_star

    def test_split_50_50(self):
        # all'ottimo drift residuo e ribilanciamenti si equivalgono
        m = _demo()
        assert m["quota_drift"] == pytest.approx(0.5)
        assert m["quota_ribil"] == pytest.approx(0.5)

    def test_scaling_radice(self):
        # raddoppiare K allunga T* di sqrt(2)
        m1 = _F["mh474_frequenza"](K, F, G, D)
        m2 = _F["mh474_frequenza"](2.0 * K, F, G, D)
        assert m2["T_star_sett"] == pytest.approx(
            math.sqrt(2.0) * m1["T_star_sett"])

    def test_drift_lento_allunga(self):
        # drift piu' lento -> si ribilancia piu' di rado
        m1 = _F["mh474_frequenza"](K, F, G, D)
        m2 = _F["mh474_frequenza"](K, F, G / 2.0, D)
        assert m2["T_star_sett"] > m1["T_star_sett"]

    def test_valori_non_validi(self):
        fq = _F["mh474_frequenza"]
        for kw in ("costo_ribil", "fuori_budget_eur", "drift_sett",
                   "dev_max"):
            base = dict(costo_ribil=K, fuori_budget_eur=F, drift_sett=G,
                        dev_max=D)
            for bad in (0.0, -1.0, float("nan"), float("inf"), True,
                        "x"):
                args = dict(base)
                args[kw] = bad
                with pytest.raises(ValueError):
                    fq(**args)
        with pytest.raises(ValueError):
            fq(K, F, G, D, settimane_anno=0.0)

    def test_costo_annuo_non_valido(self):
        ca = _F["mh474_costo_annuo"]
        a = _demo()["a_eur_sett2"]
        with pytest.raises(ValueError):
            ca(0.0, K, a)
        with pytest.raises(ValueError):
            ca(-1.0, K, a)
        with pytest.raises(ValueError):
            ca(1.0, -K, a)
        with pytest.raises(ValueError):
            ca(1.0, K, -a)
        with pytest.raises(ValueError):
            ca(1.0, True, a)


class TestVerdetto474:
    def test_demo(self):
        v = _F["mh474_verdetto"](_demo())
        assert v.startswith("RIBILANCIA")
        assert "0.8 settimane" in v  # T* = 0.795 -> ramo 0.5..2.0
        assert "130,809 EUR" in v
        assert "50%" in v

    def test_ramo_troppo_frequente(self):
        v = _F["mh474_verdetto"]({"T_star_sett": 0.2,
                                  "ribilanciamenti_anno": 260.0,
                                  "costo_annuo_ottimo": 5000.0,
                                  "quota_drift": 0.5})
        assert "piu' di una volta a settimana" in v

    def test_ramo_settimane_intere(self):
        v = _F["mh474_verdetto"]({"T_star_sett": 6.0,
                                  "ribilanciamenti_anno": 8.67,
                                  "costo_annuo_ottimo": 20000.0,
                                  "quota_drift": 0.5})
        assert "ogni 6 settimane" in v

    def test_non_valido(self):
        vd = _F["mh474_verdetto"]
        with pytest.raises(ValueError):
            vd("no")
        with pytest.raises(ValueError):
            vd({"T_star_sett": 1.0})  # chiavi mancanti
        with pytest.raises(ValueError):
            vd({"T_star_sett": float("nan"), "ribilanciamenti_anno": 1.0,
                "costo_annuo_ottimo": 1.0, "quota_drift": 0.5})
