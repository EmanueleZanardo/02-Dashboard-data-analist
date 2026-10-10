"""Test tab352 'Kelly con correlazione: due posizioni correlate': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh352_num", "mh352_kelly_f", "mh352_pq", "mh352_rho_bounds",
           "mh352_joint_probs", "mh352_logstats2", "mh352_ottimo",
           "mh352_verdetto", "mh352_confronto")

TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE348 = "Kelly con costi di trading: sizing netto"
P1 = 0.6
P2 = 0.58
WIN1 = 120.0
LOSS1 = 100.0
WIN2 = 150.0
LOSS2 = 100.0
RHO = -0.5
RHO2 = 0.5
B1 = 1.2
B2 = 1.5
F1IND = 0.26666666666666666
F2IND = 0.2999999999999999
F1OPT = 0.4
F2OPT = 0.41000000000000003
G_OPT = 0.18368330194356863
SIGMA_OPT = 0.4852579667429474
G_IND = 0.15707058653192332
SIGMA_IND = 0.3040634674942867
RHO_MIN = -0.6948083337796513
RHO_MAX = 0.9594972228385659
VERDETTO = "DIVERSIFICAZIONE: con ρ=-0.50 le due posizioni si compensano (quando una perde, l'altra tende a vincere). L'ottimo congiunto (f1=40.00%, f2=41.00%) dà g=+18.368%/round contro +15.707% (+2.66%) con σ=48.53% contro 30.41%. La correlazione negativa permette size più aggressive: più crescita attesa, ma volatilità più alta."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry352:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 362
        assert "tab352" in dvars
        assert "tab352" in withs

    def test_titoli_allineati_348_349_350_351_352(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab348")] == TITLE348
        assert titoli[dvars.index("tab349")] == TITLE349
        assert titoli[dvars.index("tab350")] == TITLE350
        assert titoli[dvars.index("tab351")] == TITLE351
        assert titoli[dvars.index("tab352")] == TITLE352

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab362"
        assert titoli[-1] == TITLE362
        assert withs[-1] == "tab362"


class TestNum:
    def test_num_ok(self):
        assert _F["mh352_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_num"](float("nan"), "x")


class TestKellyF:
    def test_kelly_demo(self):
        assert abs(_F["mh352_kelly_f"](P1, B1) - F1IND) < 1e-12
        assert abs(_F["mh352_kelly_f"](P2, B2) - F2IND) < 1e-12

    def test_kelly_no_edge(self):
        assert _F["mh352_kelly_f"](0.40, 1.2) == 0.0

    def test_kelly_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_kelly_f"](1.0, 1.2)


class TestRhoBounds:
    def test_bounds_demo(self):
        b = _F["mh352_rho_bounds"](P1, P2)
        assert abs(b["rho_min"] - RHO_MIN) < 1e-9
        assert abs(b["rho_max"] - RHO_MAX) < 1e-9

    def test_bounds_simmetrico(self):
        b = _F["mh352_rho_bounds"](0.5, 0.5)
        assert abs(b["rho_min"] - (-1.0)) < 1e-12
        assert abs(b["rho_max"] - 1.0) < 1e-12

    def test_bounds_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_rho_bounds"](0.0, 0.5)


class TestJointProbs:
    def test_demo_quattro_stati(self):
        jp = _F["mh352_joint_probs"](P1, P2, RHO)
        s = math.sqrt(P1 * (1.0 - P1) * P2 * (1.0 - P2))
        assert abs(jp["pww"] - (P1 * P2 + RHO * s)) < 1e-12
        assert abs(jp["pwl"] - (P1 * (1.0 - P2) - RHO * s)) < 1e-12
        assert abs(jp["plw"] - ((1.0 - P1) * P2 - RHO * s)) < 1e-12
        assert abs(jp["pll"] - ((1.0 - P1) * (1.0 - P2) + RHO * s)) < 1e-12

    def test_somma_uno(self):
        jp = _F["mh352_joint_probs"](P1, P2, RHO)
        assert abs(sum(jp.values()) - 1.0) < 1e-15

    def test_rho_zero_indipendenti(self):
        jp = _F["mh352_joint_probs"](P1, P2, 0.0)
        assert abs(jp["pww"] - P1 * P2) < 1e-15
        assert abs(jp["pwl"] - P1 * (1.0 - P2)) < 1e-15
        assert abs(jp["plw"] - (1.0 - P1) * P2) < 1e-15
        assert abs(jp["pll"] - (1.0 - P1) * (1.0 - P2)) < 1e-15

    def test_rho_fuori_intervallo_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_joint_probs"](P1, P2, -0.99)


class TestLogstats2:
    def test_demo_g_sigma(self):
        s = _F["mh352_logstats2"](P1, B1, F1IND, P2, B2, F2IND, RHO)
        assert abs(s["g"] - G_IND) < 1e-12
        assert abs(s["sigma"] - SIGMA_IND) < 1e-12
        assert s["sigma"] > 0.0

    def test_somma_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_logstats2"](P1, B1, 0.6, P2, B2, 0.5, RHO)

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_logstats2"](P1, B1, F1IND, P2, B2, F2IND, 0.99)


class TestOttimo:
    def test_demo(self):
        o = _F["mh352_ottimo"](P1, B1, P2, B2, RHO)
        assert abs(o["f1"] - F1OPT) < 1e-12
        assert abs(o["f2"] - F2OPT) < 1e-12
        assert abs(o["g"] - G_OPT) < 1e-9
        assert abs(o["sigma"] - SIGMA_OPT) < 1e-9
        assert o["f1"] + o["f2"] < 1.0

    def test_rho_zero_come_tab351(self):
        o = _F["mh352_ottimo"](P1, B1, P2, B2, 0.0)
        assert abs(o["f1"] - 0.24) < 1e-12
        assert abs(o["f2"] - 0.28) < 1e-12

    def test_determinismo(self):
        o1 = _F["mh352_ottimo"](P1, B1, P2, B2, RHO)
        o2 = _F["mh352_ottimo"](P1, B1, P2, B2, RHO)
        assert o1 == o2

    def test_no_edge_zeri(self):
        z = _F["mh352_ottimo"](0.40, 1.2, 0.45, 1.0, 0.0)
        assert z == {"f1": 0.0, "f2": 0.0, "g": 0.0, "sigma": 0.0}

    def test_g_ottimo_migliore(self):
        o = _F["mh352_ottimo"](P1, B1, P2, B2, RHO)
        assert o["g"] >= G_IND - 0.001

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_ottimo"](P1, B1, P2, B2, -0.99)


class TestVerdetto:
    def test_diversificazione(self):
        assert VERDETTO.startswith("DIVERSIFICAZIONE")

    def test_contagio(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO2)
        assert m["verdetto"].startswith("CONTAGIO")

    def test_nessun_edge(self):
        v = _F["mh352_verdetto"](0.0, 0.0, 0.0, 0.0, None, None,
                                 0.0, 0.0, 0.0)
        assert v.startswith("NESSUN EDGE")

    def test_solo_posizione_2(self):
        v = _F["mh352_verdetto"](0.0, 0.02, 0.0, 0.02, 0.001, 0.05,
                                 0.0011, 0.05, 0.0)
        assert v.startswith("SOLO POSIZIONE 2")

    def test_solo_posizione_1(self):
        v = _F["mh352_verdetto"](0.04, 0.0, 0.04, 0.0, 0.001, 0.05,
                                 0.0011, 0.05, 0.0)
        assert v.startswith("SOLO POSIZIONE 1")

    def test_rischio_rovina(self):
        v = _F["mh352_verdetto"](0.6, 0.6, 0.4, 0.4, None, None,
                                 0.1, 0.3, 0.5)
        assert v.startswith("RISCHIO ROVINA")

    def test_ottimo_quasi_indipendenti(self):
        v = _F["mh352_verdetto"](0.04, 0.02, 0.04, 0.02, 0.001, 0.10,
                                 0.0010001, 0.09999, 0.0)
        assert v.startswith("OTTIMO")


class TestConfronto:
    def test_demo_indipendenti(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO)
        assert abs(m["b1"] - B1) < 1e-12
        assert abs(m["b2"] - B2) < 1e-12
        assert abs(m["f1_ind"] - F1IND) < 1e-15
        assert abs(m["f2_ind"] - F2IND) < 1e-15

    def test_demo_ottimo(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO)
        assert abs(m["f1_opt"] - F1OPT) < 1e-12
        assert abs(m["f2_opt"] - F2OPT) < 1e-12
        assert abs(m["g_opt"] - G_OPT) < 1e-9
        assert abs(m["sigma_opt"] - SIGMA_OPT) < 1e-9
        assert m["verdetto"] == VERDETTO

    def test_strategie(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO)
        nomi = [s["strategia"] for s in m["strategie"]]
        assert nomi == ["Kelly indipendenti", "Half-Kelly indipendenti",
                        f"Ottimo congiunto (ρ={RHO:+.2f})"]
        assert abs(m["strategie"][1]["f1"] - F1IND / 2.0) < 1e-15

    def test_tabella_rho(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO)
        tr = m["tabella_rho"]
        assert [t["rho"] for t in tr] == [-0.5, 0.0, 0.5]
        assert abs(tr[1]["f1"] - 0.24) < 1e-12
        assert abs(tr[1]["f2"] - 0.28) < 1e-12
        assert tr[0]["g"] > tr[2]["g"]

    def test_bounds(self):
        m = _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, RHO)
        assert abs(m["rho_min"] - RHO_MIN) < 1e-9
        assert abs(m["rho_max"] - RHO_MAX) < 1e-9

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh352_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2, -0.99)

