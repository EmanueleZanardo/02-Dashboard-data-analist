"""Test tab353 'Kelly adattivo: win-rate rolling e size dinamica': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh353_num", "mh353_parse_seq", "mh353_ewma_p", "mh353_kelly_f",
           "mh353_adaptive", "mh353_verdetto", "mh353_confronto")

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
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
SEQ = 'WLLWLLWLLWWWLWWWWLWW'
B = 1.5
LAM = 0.92
PPRIOR = 0.55
FCAP = 0.4
MAXSTEP = 0.05
N = 20
NWINS = 12
PFREQ = 0.6
PEWMA = 0.6563440757052181
FSTATIC = 0.33333333333333326
FFINAL = 0.4
VERDETTO = "AUMENTO SIZE: la win-rate recente (p_ewma=65.6%) e' sopra la media storica (60.0%): il Kelly adattivo sale a f=40.00% contro f_static=33.33% (+6.67%). Il regime recente e' piu' favorevole: puoi spingere la size, restando sotto il cap."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry353:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 362
        assert "tab353" in dvars
        assert "tab353" in withs

    def test_titoli_allineati_349_350_351_352_353(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab349")] == TITLE349
        assert titoli[dvars.index("tab350")] == TITLE350
        assert titoli[dvars.index("tab351")] == TITLE351
        assert titoli[dvars.index("tab352")] == TITLE352
        assert titoli[dvars.index("tab353")] == TITLE353

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab362"
        assert titoli[-1] == TITLE362
        assert withs[-1] == "tab362"


class TestNum:
    def test_num_ok(self):
        assert _F["mh353_num"](1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_num"](float("nan"), "x")


class TestParseSeq:
    def test_misto(self):
        assert _F["mh353_parse_seq"]("Ww1Ll0") == (1, 1, 1, 0, 0, 0)

    def test_separatori(self):
        assert _F["mh353_parse_seq"]("W, L;W") == (1, 0, 1)

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"]("WX")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"](" ,;")

    def test_non_stringa_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_parse_seq"](123)


class TestEwma:
    def test_lam_1_prior_intatto(self):
        assert _F["mh353_ewma_p"]((1, 0, 1), 1.0, 0.55) == 0.55

    def test_manuale_due_passi(self):
        # 0.5 -> 0.75 -> 0.875 con lam=0.5
        assert _F["mh353_ewma_p"]((1, 1), 0.5, 0.5) == 0.875

    def test_lam_0_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((1,), 0.0, 0.5)

    def test_prior_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((1,), 0.9, 0.0)

    def test_seq_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_ewma_p"]((), 0.9, 0.5)


class TestKellyF:
    def test_demo(self):
        assert abs(_F["mh353_kelly_f"](0.6, 1.5) - 1.0 / 3.0) < 1e-12

    def test_no_edge_zero(self):
        assert _F["mh353_kelly_f"](0.3, 1.5) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_kelly_f"](0.6, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_kelly_f"](1.5, 1.5)


class TestAdaptive:
    def _demo(self):
        return _F["mh353_confronto"](SEQ, B, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_demo_numeri(self):
        m = self._demo()
        assert m["n"] == N == 20
        assert m["n_wins"] == NWINS == 12
        assert abs(m["p_freq"] - PFREQ) < 1e-12
        assert abs(m["p_ewma"] - PEWMA) < 1e-9
        assert abs(m["f_static"] - FSTATIC) < 1e-12
        assert abs(m["f_final"] - FFINAL) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("AUMENTO SIZE")

    def test_determinismo(self):
        m1 = self._demo()
        m2 = self._demo()
        assert m1["f_path"] == m2["f_path"]
        assert m1["p_path"] == m2["p_path"]

    def test_slew_rate_limit(self):
        m = self._demo()
        passi = [abs(b - a)
                 for a, b in zip(m["f_path"], m["f_path"][1:])]
        assert max(passi) <= MAXSTEP + 1e-12

    def test_cap_rispettato(self):
        m = self._demo()
        assert all(0.0 <= f <= FCAP + 1e-12 for f in m["f_path"])

    def test_f_iniziale_da_prior(self):
        m = self._demo()
        atteso = min(_F["mh353_kelly_f"](PPRIOR, B), FCAP)
        assert abs(m["f_path"][0] - atteso) < 1e-15

    def test_righe(self):
        m = self._demo()
        assert len(m["righe"]) == N
        assert [r["trade"] for r in m["righe"]] == list(range(1, N + 1))
        assert "".join(r["esito"] for r in m["righe"]) == SEQ
        assert len(m["f_path"]) == N + 1
        assert len(m["p_path"]) == N + 1

    def test_seq_corta_dati_insufficienti(self):
        m = _F["mh353_confronto"]("WLW", B, LAM, PPRIOR, FCAP, MAXSTEP)
        assert m["verdetto"].startswith("DATI INSUFFICIENTI")

    def test_seq_str_roundtrip(self):
        m = self._demo()
        assert m["seq_str"] == SEQ


class TestVerdetto:
    def test_dati_insufficienti(self):
        v = _F["mh353_verdetto"](0.10, 0.10, 0.50, 0.50, 5)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_pausa(self):
        v = _F["mh353_verdetto"](0.0, 0.10, 0.40, 0.50, 20)
        assert v.startswith("PAUSA")

    def test_aumento(self):
        v = _F["mh353_verdetto"](0.40, 1.0 / 3.0, 0.656, 0.60, 20)
        assert v.startswith("AUMENTO SIZE")

    def test_riduzione(self):
        v = _F["mh353_verdetto"](0.10, 0.20, 0.45, 0.55, 20)
        assert v.startswith("RIDUZIONE SIZE")

    def test_stabile(self):
        v = _F["mh353_verdetto"](0.20, 0.205, 0.55, 0.55, 20)
        assert v.startswith("STABILE")

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_verdetto"](-0.1, 0.1, 0.5, 0.5, 20)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_verdetto"](0.1, 0.1, 0.5, 0.5, 0)


class TestConfronto:
    def test_chiavi_e_parametri(self):
        m = _F["mh353_confronto"](SEQ, B, LAM, PPRIOR, FCAP, MAXSTEP)
        assert m["b"] == B
        assert m["lam"] == LAM
        assert m["p_prior"] == PPRIOR
        assert m["f_cap"] == FCAP
        assert m["max_step"] == MAXSTEP
        assert m["min_n"] == 10

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"]("XYZ", B, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"](SEQ, -1.0, LAM, PPRIOR, FCAP, MAXSTEP)

    def test_lam_ko(self):
        with pytest.raises(ValueError):
            _F["mh353_confronto"](SEQ, B, 1.5, PPRIOR, FCAP, MAXSTEP)

