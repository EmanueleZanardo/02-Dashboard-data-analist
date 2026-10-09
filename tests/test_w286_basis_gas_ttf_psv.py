"""Test tab286 '⛽ Basis gas TTF–PSV': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab286.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("bn286_num", "bn286_pos", "bn286_costo_trasporto",
          "bn286_psv_implicito", "bn286_basis", "bn286_margine_mwh",
          "bn286_pnl_ciclo", "bn286_be_trasporto", "bn286_be_ttf",
          "bn286_breakdown", "bn286_sensibilita_ttf", "bn286_verdetto")
bn286_num = _F["bn286_num"]
bn286_pos = _F["bn286_pos"]
bn286_costo_trasporto = _F["bn286_costo_trasporto"]
bn286_psv_implicito = _F["bn286_psv_implicito"]
bn286_basis = _F["bn286_basis"]
bn286_margine_mwh = _F["bn286_margine_mwh"]
bn286_pnl_ciclo = _F["bn286_pnl_ciclo"]
bn286_be_trasporto = _F["bn286_be_trasporto"]
bn286_be_ttf = _F["bn286_be_ttf"]
bn286_breakdown = _F["bn286_breakdown"]
bn286_sensibilita_ttf = _F["bn286_sensibilita_ttf"]
bn286_verdetto = _F["bn286_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE285 = "\U0001F6DB\uFE0F Differenziali greggio: sweet vs sour"
TITLE284 = "\U0001F3ED Unit commitment CCGT: accendere o no?"
TITLE283 = "\U0001F6E2\uFE0F Carry petrolio: contango & stoccaggio fisico"

TTF, TAR_CAP, TAR_COMM, FUEL, EXTRA, PSV = 38.0, 0.35, 0.20, 1.0, 0.15, 41.0
TRASP_ATTESO = TAR_CAP + TAR_COMM + TTF * FUEL / 100.0          # 0.93
IMPL_ATTESO = TTF + TRASP_ATTESO + EXTRA                        # 39.08
BASIS_ATTESO = PSV - IMPL_ATTESO                                # 1.92
BE_TRASP_ATTESO = PSV - TTF - EXTRA                            # 2.85
BE_TTF_ATTESO = (PSV - EXTRA - TAR_CAP - TAR_COMM) / 1.01       # 39.90099...
VOL, FISSI, SOGLIA = 10000.0, 1500.0, 0.25
MARG_ATTESO = BASIS_ATTESO - FISSI / VOL                       # 1.77
PNL_ATTESO = BASIS_ATTESO * VOL - FISSI                        # 17700.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab286:
    def test_tab286_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 326
        assert TITLE286 in titoli
        assert "tab286" in dvars
        assert "tab286" in withs
        assert titoli[dvars.index("tab286")] == TITLE286
        assert titoli[-1] == TITLE326
        keys = re.findall(r'key="(bn286_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_284_285_286(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285
        assert titoli[dvars.index("tab286")] == TITLE286


class TestBn286Validatori:
    def test_num_ok(self):
        assert bn286_num(1.92, "x") == 1.92

    def test_num_ko(self):
        with pytest.raises(ValueError):
            bn286_num(True, "x")
        with pytest.raises(ValueError):
            bn286_num(float("nan"), "x")

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            bn286_pos(-0.1, "x")

    def test_pos_zero_ok(self):
        assert bn286_pos(0.0, "x") == 0.0


class TestBn286Trasporto:
    def test_base(self):
        assert bn286_costo_trasporto(TAR_CAP, TAR_COMM, FUEL, TTF) == \
            pytest.approx(TRASP_ATTESO)

    def test_formula(self):
        # 0.5 + 0.3 + 40 * 2/100 = 1.6
        assert bn286_costo_trasporto(0.5, 0.3, 2.0, 40.0) == pytest.approx(1.6)

    def test_fuel_zero(self):
        assert bn286_costo_trasporto(0.5, 0.3, 0.0, 40.0) == pytest.approx(0.8)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bn286_costo_trasporto(-0.1, TAR_COMM, FUEL, TTF)
        with pytest.raises(ValueError):
            bn286_costo_trasporto(TAR_CAP, TAR_COMM, FUEL, -1.0)


class TestBn286Implicito:
    def test_base(self):
        assert bn286_psv_implicito(TTF, TRASP_ATTESO, EXTRA) == \
            pytest.approx(IMPL_ATTESO)

    def test_formula(self):
        assert bn286_psv_implicito(40.0, 1.0, 0.2) == pytest.approx(41.2)


class TestBn286Basis:
    def test_base(self):
        assert bn286_basis(PSV, IMPL_ATTESO) == pytest.approx(BASIS_ATTESO)

    def test_negativo_ammesso(self):
        assert bn286_basis(35.0, 39.0) == pytest.approx(-4.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            bn286_basis(-1.0, IMPL_ATTESO)


class TestBn286Margine:
    def test_base(self):
        assert bn286_margine_mwh(BASIS_ATTESO, FISSI, VOL) == \
            pytest.approx(MARG_ATTESO)

    def test_volume_zero_ko(self):
        with pytest.raises(ValueError):
            bn286_margine_mwh(BASIS_ATTESO, FISSI, 0.0)

    def test_pnl(self):
        assert bn286_pnl_ciclo(BASIS_ATTESO, VOL, FISSI) == \
            pytest.approx(PNL_ATTESO)

    def test_pnl_coerente(self):
        m = bn286_margine_mwh(BASIS_ATTESO, FISSI, VOL)
        assert bn286_pnl_ciclo(BASIS_ATTESO, VOL, FISSI) == \
            pytest.approx(m * VOL)


class TestBn286Breakeven:
    def test_be_trasporto(self):
        assert bn286_be_trasporto(PSV, TTF, EXTRA) == \
            pytest.approx(BE_TRASP_ATTESO)

    def test_be_trasporto_coerente(self):
        be = bn286_be_trasporto(PSV, TTF, EXTRA)
        assert bn286_basis(PSV, bn286_psv_implicito(TTF, be, EXTRA)) == \
            pytest.approx(0.0)

    def test_be_ttf(self):
        assert bn286_be_ttf(PSV, TAR_CAP, TAR_COMM, FUEL, EXTRA) == \
            pytest.approx(BE_TTF_ATTESO)

    def test_be_ttf_coerente(self):
        be = bn286_be_ttf(PSV, TAR_CAP, TAR_COMM, FUEL, EXTRA)
        tr = bn286_costo_trasporto(TAR_CAP, TAR_COMM, FUEL, be)
        assert bn286_basis(PSV, bn286_psv_implicito(be, tr, EXTRA)) == \
            pytest.approx(0.0, abs=1e-9)

    def test_piu_psv_piu_break_even(self):
        assert bn286_be_trasporto(PSV + 2.0, TTF, EXTRA) > BE_TRASP_ATTESO


class TestBn286Breakdown:
    def test_chiavi(self):
        b = bn286_breakdown(TTF, TAR_CAP, TAR_COMM, TTF * FUEL / 100.0,
                            EXTRA, IMPL_ATTESO, BASIS_ATTESO)
        assert set(b) == {"ttf", "tariffa_capacita", "tariffa_commodity",
                          "fuel_in_kind", "oneri_extra", "psv_implicito",
                          "basis"}

    def test_somma_componenti(self):
        b = bn286_breakdown(TTF, TAR_CAP, TAR_COMM, TTF * FUEL / 100.0,
                            EXTRA, IMPL_ATTESO, BASIS_ATTESO)
        somma = (b["ttf"] + b["tariffa_capacita"] + b["tariffa_commodity"]
                 + b["fuel_in_kind"] + b["oneri_extra"])
        assert somma == pytest.approx(b["psv_implicito"])


class TestBn286Sensibilita:
    def test_punti_e_centro(self):
        righe = bn286_sensibilita_ttf(TTF, TAR_CAP, TAR_COMM, FUEL, EXTRA, PSV)
        assert len(righe) == 9
        assert righe[4]["ttf"] == pytest.approx(TTF)
        assert righe[4]["basis"] == pytest.approx(BASIS_ATTESO)

    def test_monotona_decrescente(self):
        righe = bn286_sensibilita_ttf(TTF, TAR_CAP, TAR_COMM, FUEL, EXTRA, PSV)
        margini = [r["basis"] for r in righe]
        assert all(a > b for a, b in zip(margini, margini[1:]))

    def test_estremi(self):
        righe = bn286_sensibilita_ttf(TTF, TAR_CAP, TAR_COMM, FUEL, EXTRA, PSV)
        assert righe[0]["ttf"] == pytest.approx(TTF * 0.85)
        assert righe[-1]["ttf"] == pytest.approx(TTF * 1.15)

    def test_n_punti_ko(self):
        with pytest.raises(ValueError):
            bn286_sensibilita_ttf(TTF, TAR_CAP, TAR_COMM, FUEL, EXTRA, PSV,
                                  n_punti=2)


class TestBn286Verdetto:
    def test_positivo(self):
        r = bn286_verdetto(MARG_ATTESO, SOGLIA)
        assert r["verdetto"] == "positivo"

    def test_in_linea(self):
        r = bn286_verdetto(0.10, SOGLIA)
        assert r["verdetto"] == "in_linea"

    def test_negativo(self):
        r = bn286_verdetto(-0.5, SOGLIA)
        assert r["verdetto"] == "negativo"

    def test_soglia_bordo(self):
        r = bn286_verdetto(SOGLIA, SOGLIA)
        assert r["verdetto"] == "positivo"

    def test_soglia_negativa_ko(self):
        with pytest.raises(ValueError):
            bn286_verdetto(MARG_ATTESO, -0.1)
