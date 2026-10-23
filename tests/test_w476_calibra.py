"""Test tab476 '🎯 Calibrazione: previsto vs realizzato': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh476_num", "mh476_riga", "mh476_statistiche",
           "mh476_calibra_c", "mh476_verdetto")

TITLE476 = "🎯 Calibrazione: previsto vs realizzato"
TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"

# Righe demo deterministiche: previsto dal modello tab475 (spread B
# 178.77 / C 255.07 / D 11.61 EUR, impact B 1'710.28 / C 2'415.34 /
# D 41.70 EUR, nozionale = trade B 715'069 / C 637'664 / D 77'405 EUR);
# realizzato a consuntivo con impact sopra il previsto -> il modello con
# c_impact=1.0 SOTTOSTIMA, k stimato ~1.20
PSB = 178.76727721713766
PIB = 1710.2792188152227
RSB = 185.2
RIB = 2050.0
NZB = 715069.1088685506
PSC = 255.06550210120346
PIC = 2415.34324799556
RSC = 248.9
RIC = 2890.5
NZC = 637663.7552530087
PSD = 11.610806042331268
PID = 41.703480377612024
RSD = 12.05
RID = 55.8
NZD = 77405.37361554179
EB = 346.1535039676394
EBB = 4.840839852743128
EC = 468.9912499032366
ECB = 7.354836244646725
ED = 14.5357135800567
EDB = 1.8778687965841891
PTOT = 4612.769532549067
RTOT = 5442.45
BTOT = 829.6804674509331
BPCT = 17.986601359475305
RMSE = 336.64339577865684
MAE = 276.56015581697756
RBPS = 5.1978757803119215
HIT = 0.6666666666666666
BSP = 0.706414639327603
BIM = 828.9740528116052
K476 = 1.197390210932288
R2_476 = 0.9999902087016025
NEFF = 3
VERD476 = 'SOTTOSTIMA — il modello sottostima i costi reali del 18.0% (bias 830 EUR); moltiplica c_impact di tab475 per 1.197 (r²=1.00 su 3 righe)'

RIGHE = (("B", PSB, PIB, RSB, RIB, NZB),
         ("C", PSC, PIC, RSC, RIC, NZC),
         ("D", PSD, PID, RSD, RID, NZD))


def _righe():
    return [_F["mh476_riga"](*r) for r in RIGHE]


class TestRegistry476:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 656
        assert "tab476" in dvars
        assert "tab476" in withs

    def test_titoli_allineati_472_473_474_475_476(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {472: TITLE472, 473: TITLE473, 474: TITLE474,
                  475: TITLE475, 476: TITLE476}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 5


class TestNum476:
    def test_accetta_numeri(self):
        assert _F["mh476_num"](3, "x") == 3.0
        assert _F["mh476_num"](2.5, "x") == 2.5
        assert _F["mh476_num"](0, "x") == 0.0

    def test_rifiuta(self):
        for bad in (True, "3", None, float("nan"), float("inf"),
                    float("-inf")):
            with pytest.raises(ValueError):
                _F["mh476_num"](bad, "x")


class TestRiga476:
    def test_campi(self):
        r = _F["mh476_riga"](*RIGHE[0])
        assert r["nome"] == "B"
        assert r["previsto_tot"] == PSB + PIB
        assert r["realizzato_tot"] == RSB + RIB
        assert r["err_tot"] == EB
        assert r["err_bps"] == EBB
        assert r["err_spread"] == RSB - PSB
        assert r["err_impact"] == RIB - PIB

    def test_nome_strip(self):
        r = _F["mh476_riga"]("  E  ", 1.0, 2.0, 1.0, 2.0, 100.0)
        assert r["nome"] == "E"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh476_riga"]("X", -1.0, 2.0, 1.0, 2.0, 100.0)
        with pytest.raises(ValueError):
            _F["mh476_riga"]("X", 1.0, 2.0, 1.0, -2.0, 100.0)
        with pytest.raises(ValueError):
            _F["mh476_riga"]("X", 1.0, 2.0, 1.0, 2.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh476_riga"]("", 1.0, 2.0, 1.0, 2.0, 100.0)
        with pytest.raises(ValueError):
            _F["mh476_riga"]("   ", 1.0, 2.0, 1.0, 2.0, 100.0)
        with pytest.raises(ValueError):
            _F["mh476_riga"](None, 1.0, 2.0, 1.0, 2.0, 100.0)


class TestStatistiche476:
    def test_somme(self):
        s = _F["mh476_statistiche"](_righe())
        assert s["n"] == 3
        assert s["previsto_tot"] == PTOT
        assert s["realizzato_tot"] == RTOT
        assert s["bias_tot"] == BTOT
        assert s["bias_pct"] == BPCT
        assert s["bias_spread"] == BSP
        assert s["bias_impact"] == BIM

    def test_errori(self):
        s = _F["mh476_statistiche"](_righe())
        assert s["rmse_eur"] == RMSE
        assert s["mae_eur"] == MAE
        assert s["rmse_bps"] == RBPS
        assert s["hit_rate"] == HIT

    def test_chiave_fatta_a_mano(self):
        # RMSE e MAE ricalcolati a mano (niente helper 476)
        errs = [EB, EC, ED]
        rmse_mano = math.sqrt(sum(e * e for e in errs) / 3)
        mae_mano = sum(abs(e) for e in errs) / 3
        s = _F["mh476_statistiche"](_righe())
        assert abs(s["rmse_eur"] - rmse_mano) < 1e-9
        assert abs(s["mae_eur"] - mae_mano) < 1e-9
        assert abs(s["bias_pct"] - (RTOT - PTOT) / PTOT * 100.0) < 1e-9

    def test_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh476_statistiche"]([])

    def test_previsto_nullo(self):
        rz = [_F["mh476_riga"]("Z", 0.0, 0.0, 0.0, 0.0, 100.0)]
        with pytest.raises(ValueError):
            _F["mh476_statistiche"](rz)

    def test_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh476_statistiche"](_righe(), tolleranza_bps=-1.0)


class TestCalibra476:
    def test_k(self):
        c = _F["mh476_calibra_c"](_righe())
        assert c["k"] == K476
        assert c["n_eff"] == NEFF
        # chiave: k = Σ(pr)/Σ(pp) a mano
        prs = [(PIB, RIB), (PIC, RIC), (PID, RID)]
        k_mano = sum(p * r for p, r in prs) / sum(p * p for p, r in prs)
        assert abs(c["k"] - k_mano) < 1e-12

    def test_r2(self):
        assert _F["mh476_calibra_c"](_righe())["r2"] == R2_476
        assert 0.0 <= R2_476 <= 1.0

    def test_suggerimento(self):
        c = _F["mh476_calibra_c"](_righe())
        assert "c_impact" in c["suggerimento"]
        assert f"{K476:.3f}" in c["suggerimento"]

    def test_degeneri(self):
        rz = [_F["mh476_riga"]("Z", 10.0, 0.0, 12.0, 0.0, 100.0)]
        with pytest.raises(ValueError):
            _F["mh476_calibra_c"](rz)
        with pytest.raises(ValueError):
            _F["mh476_calibra_c"]([])


class TestVerdetto476:
    def test_demo_sottostima(self):
        righe = _righe()
        s = _F["mh476_statistiche"](righe)
        c = _F["mh476_calibra_c"](righe)
        v = _F["mh476_verdetto"](s, c)
        assert v == VERD476
        assert v.startswith("SOTTOSTIMA")
        assert BPCT > 10.0

    def test_dati_insufficienti(self):
        s = _F["mh476_statistiche"](_righe()[:2])
        v = _F["mh476_verdetto"](s, None)
        assert v.startswith("DATI INSUFFICIENTI")

    def test_calibrato(self):
        s = {"n": 5, "bias_pct": 3.0, "bias_tot": 100.0,
             "hit_rate": 0.8, "rmse_bps": 2.0}
        v = _F["mh476_verdetto"](s, None)
        assert v.startswith("CALIBRATO")

    def test_sovrastima(self):
        s = {"n": 4, "bias_pct": -15.0, "bias_tot": -300.0,
             "hit_rate": 0.5, "rmse_bps": 4.0}
        v = _F["mh476_verdetto"](s, None)
        assert v.startswith("SOVRASTIMA")

    def test_soglia_esatta(self):
        s = {"n": 4, "bias_pct": 10.0, "bias_tot": 200.0,
             "hit_rate": 0.5, "rmse_bps": 4.0}
        assert _F["mh476_verdetto"](s, None).startswith("CALIBRATO")

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh476_verdetto"]({}, None)
        with pytest.raises(ValueError):
            _F["mh476_verdetto"]({"n": 3}, None)
        with pytest.raises(ValueError):
            s = _F["mh476_statistiche"](_righe())
            _F["mh476_verdetto"](s, "k")
        with pytest.raises(ValueError):
            s = _F["mh476_statistiche"](_righe())
            _F["mh476_verdetto"](s, None, tol_bias_pct=-1.0)


class TestDeterminismo476:
    def test_determinismo(self):
        r1 = _F["mh476_riga"](*RIGHE[1])
        r2 = _F["mh476_riga"](*RIGHE[1])
        assert r1 == r2
        s1 = _F["mh476_statistiche"](_righe())
        s2 = _F["mh476_statistiche"](_righe())
        assert s1 == s2
        assert (_F["mh476_calibra_c"](_righe()) ==
                _F["mh476_calibra_c"](_righe()))
