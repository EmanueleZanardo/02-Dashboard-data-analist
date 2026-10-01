"""Test casi limite di calcola_drawdown_mtm (stile pytest).

La tab130 ha gia' un test dedicato (36 check); qui si coprono i casi limite:
curve monotone, recupero/non recupero, soglie, input non validi, NaN,
e la coerenza interna max_drawdown == profondita' dell'episodio peggiore.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

calcola_drawdown_mtm = load("calcola_drawdown_mtm")["calcola_drawdown_mtm"]
ddf = calcola_drawdown_mtm


def curva(valori, start="2026-01-01"):
    idx = pd.date_range(start, periods=len(valori), freq="D")
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


class TestDrawdownCasiLimite:
    def test_sempre_crescente_nessun_drawdown(self):
        d = ddf(curva([0.0, 10.0, 20.0, 30.0]))
        assert d["errore"] is None and d["valido"]
        assert d["max_drawdown"] == 0.0
        assert d["episodi"] == []
        assert d["drawdown_attuale"] == 0.0
        assert d["n_episodi_soglia"] == 0
        assert (d["drawdown"] <= 0).all().all()

    def test_sempre_decrescente(self):
        d = ddf(curva([30.0, 20.0, 10.0, 0.0]))
        assert d["max_drawdown"] == pytest.approx(-30.0)  # ultimo - primo
        assert d["picco_data"] == pd.Timestamp("2026-01-01")
        assert d["minimo_data"] == pd.Timestamp("2026-01-04")
        assert d["recupero_data"] is None
        assert d["recupero_giorni"] is None
        assert d["durata_max_giorni"] == 3
        assert d["drawdown_attuale"] == pytest.approx(-30.0)
        assert len(d["episodi"]) == 1
        assert d["episodi"][0]["recuperato"] is False

    def test_v_con_recupero(self):
        d = ddf(curva([0.0, -10.0, -5.0, 5.0]))
        assert d["max_drawdown"] == pytest.approx(-10.0)
        assert d["picco_valore"] == pytest.approx(0.0)
        assert d["minimo_valore"] == pytest.approx(-10.0)
        assert d["recupero_data"] == pd.Timestamp("2026-01-04")
        assert d["recupero_giorni"] == 3
        assert d["durata_max_giorni"] == 1
        assert len(d["episodi"]) == 1
        assert d["episodi"][0]["recuperato"] is True
        assert d["episodi"][0]["profondita"] == pytest.approx(10.0)

    def test_coerenza_max_con_episodio_peggiore(self):
        d = ddf(curva([0.0, 5.0, 3.0, 8.0, 2.0, 9.0]))
        assert len(d["episodi"]) == 2
        profondita = sorted(e["profondita"] for e in d["episodi"])
        assert profondita == pytest.approx([2.0, 6.0])
        assert d["max_drawdown"] == pytest.approx(-max(profondita))
        assert d["n_episodi_soglia"] == 2          # soglia 0: tutti
        assert len(d["df_episodi"]) == 2

    def test_running_max_monotono(self):
        d = ddf(curva([0.0, 5.0, 3.0, 8.0, 2.0, 9.0, 1.0]))
        rm = d["running_max"].to_numpy()
        assert (np.diff(rm) >= 0).all()
        assert (d["drawdown"] <= 1e-12).all().all()

    def test_soglia_filtra_episodi(self):
        d = ddf(curva([0.0, -100.0, 0.0]), soglia_eur=50.0)
        assert d["n_episodi_soglia"] == 1
        d2 = ddf(curva([0.0, -100.0, 0.0]), soglia_eur=200.0)
        assert d2["n_episodi_soglia"] == 0
        assert len(d2["episodi"]) == 1  # gli episodi restano, filtra solo il df

    def test_nan_droppati(self):
        d = ddf(curva([1.0, np.nan, 3.0, 2.0]))
        assert d["valido"]
        assert d["max_drawdown"] == pytest.approx(-1.0)

    def test_piatta(self):
        d = ddf(curva([5.0, 5.0, 5.0, 5.0]))
        assert d["valido"]
        assert d["max_drawdown"] == 0.0
        assert d["episodi"] == []


class TestDrawdownErrori:
    def test_serie_vuota(self):
        d = ddf(pd.Series([], dtype=float))
        assert not d["valido"] and d["errore"] is not None

    def test_un_solo_punto(self):
        d = ddf(curva([5.0]))
        assert not d["valido"] and "2 punti" in d["errore"]

    def test_valori_infiniti(self):
        d = ddf(curva([1.0, np.inf, 3.0]))
        assert not d["valido"] and d["errore"] is not None

    def test_non_numerica(self):
        d = ddf(pd.Series(["a", "b", "c"]))
        assert not d["valido"] and d["errore"] is not None

    def test_soglia_negativa(self):
        d = ddf(curva([0.0, -5.0, 2.0]), soglia_eur=-1.0)
        assert not d["valido"] and d["errore"] is not None

    def test_soglia_nan(self):
        d = ddf(curva([0.0, -5.0, 2.0]), soglia_eur=float("nan"))
        assert not d["valido"] and d["errore"] is not None
