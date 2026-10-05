"""Test tab244 'Acconto & conguaglio': funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
La tab244 era stata aggiunta nel ciclo 18:40 senza test dedicato: questo file
colma il gap testando a244_sintesi + profilo_mensile_demo.
"""

import pytest

from appfuncs import load

_F = load("a244_sintesi", "profilo_mensile_demo")
a244_sintesi = _F["a244_sintesi"]
profilo_mensile_demo = _F["profilo_mensile_demo"]


def _q(tipo="invernale"):
    return profilo_mensile_demo(tipo)


class TestA244Sintesi:
    def test_var_zero_conguaglio_zero(self):
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=0.0)
        assert s["conguaglio"] == pytest.approx(0.0, abs=0.01)
        assert s["acconto_base"] == pytest.approx(s["acconto_ottimale"], rel=1e-9)

    def test_var_positiva_conguaglio_atteso(self):
        # +10% di 60000 kWh a 0.28 €/kWh -> 1680 € a debito (il fisso non varia)
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=10.0)
        assert s["conguaglio"] == pytest.approx(1680.0, abs=0.05)
        assert s["costo_annuo_reale"] - s["costo_annuo_stimato"] == pytest.approx(1680.0, abs=0.05)

    def test_var_negativa_conguaglio_a_credito(self):
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=-10.0)
        assert s["conguaglio"] == pytest.approx(-1680.0, abs=0.05)

    def test_ricalibrazione_azzecca_conguaglio(self):
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=10.0,
                          mese_ricalcolo=3)
        assert s["ricalcolato"] is True
        assert abs(s["conguaglio"]) < 0.05

    def test_senza_ricalibrazione_flag_falso(self):
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=10.0)
        assert s["ricalcolato"] is False

    def test_serie_mensili_12_valori(self):
        s = a244_sintesi(60000.0, _q(), 0.28, 600.0, 5, var_consumo_pct=10.0)
        for k in ("kwh_stim_mese", "kwh_real_mese", "costo_real_mese",
                  "versato_mese", "saldo_progressivo"):
            assert len(s[k]) == 12
        assert sum(s["kwh_stim_mese"]) == pytest.approx(60000.0, rel=1e-3)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            a244_sintesi(0.0, _q(), 0.28, 600.0, 5)
        with pytest.raises(ValueError):
            a244_sintesi(60000.0, [0.1] * 11, 0.28, 600.0, 5)
        with pytest.raises(ValueError):
            a244_sintesi(60000.0, _q(), -0.1, 600.0, 5)
        with pytest.raises(ValueError):
            a244_sintesi(60000.0, _q(), 0.28, 600.0, 12)


class TestProfiloMensileDemo:
    def test_quote_sommano_a_uno(self):
        for tipo in ("piatto", "estivo", "invernale", "doppia_punta", "sconosciuto"):
            q = profilo_mensile_demo(tipo)
            assert len(q) == 12
            assert sum(q) == pytest.approx(1.0, rel=1e-9)
