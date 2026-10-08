"""Test tab295 '🧪🛡️ Backtest dell'ES: la coda e' sottostimata?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab295. Backtest di Acerbi-Szekely (2014) su Z1/Z2.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("es295_num", "es295_pos", "es295_conf", "es295_parse_pnl",
          "es295_perdite", "es295_parametri", "es295_superamenti",
          "es295_z1", "es295_z2", "es295_norm_cdf",
          "es295_pvalue_asintotico", "es295_verdetto")
es295_num = _F["es295_num"]
es295_pos = _F["es295_pos"]
es295_conf = _F["es295_conf"]
es295_parse_pnl = _F["es295_parse_pnl"]
es295_perdite = _F["es295_perdite"]
es295_parametri = _F["es295_parametri"]
es295_superamenti = _F["es295_superamenti"]
es295_z1 = _F["es295_z1"]
es295_z2 = _F["es295_z2"]
es295_norm_cdf = _F["es295_norm_cdf"]
es295_pvalue_asintotico = _F["es295_pvalue_asintotico"]
es295_verdetto = _F["es295_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"

DEMO = [320, -150, 480, -600, 210, -90, 540, -2600, 130, -320,
        410, -180, 95, -730, 260, -410, 380, -120, 510, -3100,
        -240, 170, -520, 290, -140, 660, -2800, 120, -390, 440,
        -210, 180, -640, 350, -260, 720, -4100, 90, -330, 260,
        -180, 470, -290, 130, -540, 390, -2700, 220, -160, 510,
        -350, 140, -230, 690, -2600, 110, -420, 380, -190, -3300]
DEMO_TXT = "\n".join(str(v) for v in DEMO)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab295:
    def test_tab295_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 298
        assert TITLE295 in titoli
        assert "tab295" in dvars
        assert "tab295" in withs
        assert titoli[dvars.index("tab295")] == TITLE295
        assert titoli[-1] == TITLE298
        keys = re.findall(r'key="(es295_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_293_294_295(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab293")] == TITLE293
        assert titoli[dvars.index("tab294")] == TITLE294
        assert titoli[dvars.index("tab295")] == TITLE295


class TestEs295Validatori:
    def test_num_ok(self):
        assert es295_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            es295_num(True, "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            es295_num(float("inf"), "x")

    def test_pos_negativo_ko(self):
        with pytest.raises(ValueError):
            es295_pos(-1.0, "x")

    def test_conf_ok(self):
        assert es295_conf(0.975) == 0.975

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            es295_conf(1.0)
        with pytest.raises(ValueError):
            es295_conf(0.0)


class TestEs295Parse:
    def test_ok_virgole_commenti(self):
        vals = es295_parse_pnl("# cmt\n\n1,5\n" + "\n".join(["2"] * 19))
        assert len(vals) == 20
        assert vals[0] == pytest.approx(1.5)

    def test_troppo_pochi_ko(self):
        with pytest.raises(ValueError):
            es295_parse_pnl("\n".join(["1"] * 19))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            es295_parse_pnl("\n".join(["1"] * 19 + ["abc"]))


class TestEs295Perdite:
    def test_conversione(self):
        assert es295_perdite([100.0, -50.0, 0.0]) == [-100.0, 50.0, -0.0]

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            es295_perdite([])


class TestEs295Parametri:
    def test_ok(self):
        p = es295_parametri(2000.0, 3200.0, 0.975)
        assert p == {"var": 2000.0, "es": 3200.0, "conf": 0.975,
                     "atteso": pytest.approx(0.025)}

    def test_es_uguale_var_ok(self):
        assert es295_parametri(2000.0, 2000.0, 0.95)["es"] == 2000.0

    def test_es_minore_var_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(3200.0, 2000.0, 0.975)

    def test_var_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(0.0, 3200.0, 0.975)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            es295_parametri(2000.0, 3200.0, 1.0)


class TestEs295Superamenti:
    def test_conteggio(self):
        r = es295_superamenti([100.0, 2500.0, 50.0, 2600.0, 300.0], 2000.0)
        assert r["n"] == 5
        assert r["N"] == 2
        assert r["tasso"] == pytest.approx(0.4)
        assert r["indici"] == [1, 3]

    def test_uguaglianza_non_supera(self):
        r = es295_superamenti([2000.0, 2000.01], 2000.0)
        assert r["N"] == 1
        assert r["indici"] == [1]


class TestEs295Z1:
    def test_sintetico_valori_noti(self):
        # perdite [50,150,250,30], var=100, es=200, conf=0.9:
        # Y = [0, 7.5, 12.5, 0] -> media 5 -> Z1 = 4
        r = es295_z1([50.0, 150.0, 250.0, 30.0], 100.0, 200.0, 0.9)
        assert r["n"] == 4
        assert r["N"] == 2
        assert r["z1"] == pytest.approx(4.000000000000001)
        assert r["media_y"] == pytest.approx(5.0)
        assert r["s_y"] == pytest.approx(6.123724356957946)

    def test_zero_sotto_h0_costruita(self):
        # 2 superamenti al 5% con perdita = ES -> media(Y) = 1 -> Z1 = 0
        perd = [200.0, 200.0] + [10.0] * 38
        r = es295_z1(perd, 100.0, 200.0, 0.95)
        assert r["N"] == 2
        assert r["z1"] == pytest.approx(0.0, abs=1e-12)

    def test_es_minore_var_ko(self):
        with pytest.raises(ValueError):
            es295_z1([150.0] * 20, 200.0, 100.0, 0.95)


class TestEs295Z2:
    def test_sintetico_valori_noti(self):
        # W = [0.75, 1.25] -> media 1 -> Z2 = 0
        r = es295_z2([50.0, 150.0, 250.0, 30.0], 100.0, 200.0)
        assert r["N"] == 2
        assert r["z2"] == pytest.approx(0.0, abs=1e-12)
        assert r["media_w"] == pytest.approx(1.0)
        assert r["s_w"] == pytest.approx(0.3535533905932738)

    def test_nessun_superamento_ko(self):
        with pytest.raises(ValueError):
            es295_z2([10.0, 20.0, 30.0], 100.0, 200.0)

    def test_singolo_superamento_s_zero(self):
        r = es295_z2([500.0] + [10.0] * 25, 100.0, 200.0)
        assert r["N"] == 1
        assert r["s_w"] == 0.0


class TestEs295NormCdf:
    def test_zero(self):
        assert es295_norm_cdf(0.0) == pytest.approx(0.5)

    def test_valore_noto(self):
        assert es295_norm_cdf(1.6448536269514729) == pytest.approx(0.95)

    def test_simmetria(self):
        assert es295_norm_cdf(-1.2) == pytest.approx(1.0 - es295_norm_cdf(1.2))


class TestEs295Pvalue:
    def test_stat_zero_p_mezo(self):
        r = es295_pvalue_asintotico(0.0, 40, 1.5)
        assert r["z"] == pytest.approx(0.0)
        assert r["p"] == pytest.approx(0.5)

    def test_sintetico(self):
        r = es295_pvalue_asintotico(4.000000000000001, 4, 6.123724356957946)
        assert r["z"] == pytest.approx(1.3063945294843617)
        assert r["p"] == pytest.approx(0.09570921261880372)

    def test_s_nulla_ko(self):
        with pytest.raises(ValueError):
            es295_pvalue_asintotico(1.0, 10, 0.0)

    def test_n_eff_troppo_piccolo_ko(self):
        with pytest.raises(ValueError):
            es295_pvalue_asintotico(1.0, 1, 0.5)


class TestEs295Verdetto:
    def test_coerente(self):
        r = es295_verdetto(0.5, 0.4, 7)
        assert r["verdetto"] == "coda coerente col modello"
        assert r["pmin"] == pytest.approx(0.4)

    def test_zona_gialla(self):
        assert es295_verdetto(0.03, None, 7)["verdetto"].startswith("zona gialla")

    def test_sottostimata_prende_minimo(self):
        r = es295_verdetto(0.5, 0.005, 7)
        assert r["verdetto"].startswith("coda sottostimata")
        assert r["pmin"] == pytest.approx(0.005)

    def test_nessun_superamento(self):
        r = es295_verdetto(None, None, 0)
        assert r["verdetto"] == "nessun superamento: modello conservativo"
        assert r["pmin"] is None

    def test_dati_insufficienti(self):
        assert es295_verdetto(None, None, 7)["verdetto"] == \
            "dati insufficienti per il test"

    def test_p_fuori_range_ko(self):
        with pytest.raises(ValueError):
            es295_verdetto(1.5, None, 7)


class TestEs295Integrazione:
    def test_catena_demo(self):
        pnl = es295_parse_pnl(DEMO_TXT)
        assert len(pnl) == 60
        perd = es295_perdite(pnl)
        sup = es295_superamenti(perd, 2000.0)
        assert sup["N"] == 7
        z1 = es295_z1(perd, 2000.0, 3200.0, 0.975)
        assert z1["z1"] == pytest.approx(3.4166666666666625)
        assert z1["s_y"] == pytest.approx(12.443658335407692)
        z2 = es295_z2(perd, 2000.0, 3200.0)
        assert z2["N"] == 7
        assert z2["z2"] == pytest.approx(-0.0535714285714286)
        r1 = es295_pvalue_asintotico(z1["z1"], z1["n"], z1["s_y"])
        assert r1["p"] == pytest.approx(0.016717638577597338)
        r2 = es295_pvalue_asintotico(z2["z2"], z2["N"], z2["s_w"])
        v = es295_verdetto(r1["p"], r2["p"], z1["N"])
        assert v["verdetto"] == "zona gialla: coda piu' pesante del modello"
