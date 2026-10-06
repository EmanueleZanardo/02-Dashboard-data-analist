"""Test tab226 (stile pytest): Accise e IVA.

Funzione pura calcola_accise_iva estratta da app.py via AST (tests/appfuncs).
Stile QA: numeri calcolati a mano + validazione input + determinismo +
registry tab226.
"""

import re
from pathlib import Path

from appfuncs import load

_F = load("calcola_accise_iva")
calcola_accise_iva = _F["calcola_accise_iva"]


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_residente_sotto_esenzione(self):
        # 1800 kWh/anno = 150/mese -> tutta esente
        r = calcola_accise_iva(1800.0, "domestica_residente")
        assert r["valido"] and r["errore"] is None
        assert r["accisa_annua"] == 0.0
        assert r["aliquota_iva_usata"] == 10.0

    def test_residente_sopra_esenzione(self):
        # 2400 kWh/anno = 200/mese -> 50*12=600 kWh * 0.0227 = 13.62
        r = calcola_accise_iva(2400.0, "domestica_residente")
        assert abs(r["accisa_annua"] - 13.62) < 1e-9

    def test_non_residente(self):
        # 2400 kWh * 0.0227 = 54.48
        r = calcola_accise_iva(2400.0, "domestica_non_residente")
        assert abs(r["accisa_annua"] - 54.48) < 1e-9

    def test_non_domestica_sotto_soglia(self):
        # 12000 kWh * 0.0125 = 150.0
        r = calcola_accise_iva(12000.0, "non_domestica")
        assert abs(r["accisa_annua"] - 150.0) < 1e-9
        assert r["aliquota_iva_usata"] == 22.0

    def test_non_domestica_sopra_soglia(self):
        # 15M/anno = 1.25M/mese: 1.2M*0.0125 + 50k*0.0075 = 15375/mese
        r = calcola_accise_iva(15000000.0, "non_domestica")
        assert abs(r["accisa_annua"] - 184500.0) < 1e-6

    def test_illuminazione_pubblica_esente(self):
        r = calcola_accise_iva(50000.0, "illuminazione_pubblica")
        assert r["accisa_annua"] == 0.0

    def test_iva_su_base_con_accisa(self):
        # base = 2400 + 600 + 150 = 3150 -> IVA 22% = 693.0
        r = calcola_accise_iva(12000.0, "non_domestica",
                               costo_energia_eur=2400.0, altri_oneri_eur=600.0)
        assert abs(r["iva_eur"] - 693.0) < 1e-9
        assert abs(r["base_imponibile_eur"] - 3150.0) < 1e-9
        assert abs(r["totale_imposte"] - 843.0) < 1e-9
        assert abs(r["quota_fiscale_pct"] - 843.0 / 3843.0 * 100) < 1e-9

    def test_iva_domestica_10(self):
        # base = 576 + 0 + 13.62 = 589.62 -> IVA 10% = 58.962
        r = calcola_accise_iva(2400.0, "domestica_residente",
                               costo_energia_eur=576.0)
        assert abs(r["iva_eur"] - 58.962) < 1e-9

    def test_aliquota_custom(self):
        r = calcola_accise_iva(12000.0, "non_domestica", aliquota_iva=10.0)
        assert r["aliquota_iva_usata"] == 10.0
        assert abs(r["iva_eur"] - (150.0 * 0.10)) < 1e-9

    def test_accise_custom(self):
        acc = {"dom_esenzione_kwh_mese": 0.0, "dom_aliquota": 0.05,
               "nd_soglia_kwh_mese": 1000.0, "nd_aliquota_1": 0.02,
               "nd_aliquota_2": 0.01}
        r = calcola_accise_iva(24000.0, "non_domestica", accise=acc)
        # 2000/mese: 1000*0.02 + 1000*0.01 = 30/mese -> 360/anno
        assert abs(r["accisa_annua"] - 360.0) < 1e-9

    def test_verdetti(self):
        r = calcola_accise_iva(1800.0, "domestica_residente")
        assert "LEGGERO" in r["verdetto"]
        r = calcola_accise_iva(12000.0, "non_domestica",
                               costo_energia_eur=2400.0, altri_oneri_eur=600.0)
        assert "PESANTE" in r["verdetto"]  # 843/3843 = 21.9%

    def test_mensile_e_sensitivita(self):
        r = calcola_accise_iva(12000.0, "non_domestica")
        assert len(r["df_mensile"]) == 12
        assert abs(r["df_mensile"]["Accisa (€)"].sum() - 150.0) < 0.06
        assert len(r["df_sensitivita"]) == 5
        base = r["df_sensitivita"].iloc[2]
        assert base["Scenario"] == "base"
        assert abs(base["Accisa (€)"] - 150.0) < 0.06
        # scenari estremi coerenti: -30% -> 8400 kWh * 0.0125 = 105
        meno30 = r["df_sensitivita"].iloc[0]
        assert abs(meno30["Accisa (€)"] - 105.0) < 0.06

    def test_determinismo(self):
        kw = dict(tipo_utenza="non_domestica", costo_energia_eur=2400.0)
        a = calcola_accise_iva(12000.0, **kw)
        b = calcola_accise_iva(12000.0, **kw)
        assert a["totale_imposte"] == b["totale_imposte"]
        assert a["verdetto"] == b["verdetto"]


# ------------------------------------------------------- input invalidi
class TestInputInvalidi:
    def test_energia_zero_negativa(self):
        assert calcola_accise_iva(0.0)["errore"] is not None
        assert calcola_accise_iva(-5.0)["errore"] is not None

    def test_tipo_utenza_invalido(self):
        r = calcola_accise_iva(1000.0, "atlantide")
        assert r["errore"] is not None and r["valido"] is False

    def test_costi_negativi(self):
        assert calcola_accise_iva(1000.0, costo_energia_eur=-1)["errore"]
        assert calcola_accise_iva(1000.0, altri_oneri_eur=-1)["errore"]

    def test_accise_non_dict_e_negative(self):
        assert calcola_accise_iva(1000.0, accise="x")["errore"] is not None
        bad = {"nd_aliquota_1": -0.5}
        assert calcola_accise_iva(1000.0, accise=bad)["errore"] is not None

    def test_aliquota_iva_fuori_range(self):
        assert calcola_accise_iva(1000.0, aliquota_iva=150)["errore"]
        assert calcola_accise_iva(1000.0, aliquota_iva=-1)["errore"]

    def test_energia_non_numerica(self):
        assert calcola_accise_iva("mille")["errore"] is not None
        assert calcola_accise_iva(float("nan"))["errore"] is not None
        assert calcola_accise_iva(True)["errore"] is not None

    def test_scenari_invalidi(self):
        r = calcola_accise_iva(1000.0, energia_scenari=[])
        assert r["valido"] and len(r["df_sensitivita"]) == 0
        r = calcola_accise_iva(1000.0, energia_scenari=[-100.0])
        assert r["errore"] is not None  # energia scenario <= 0


# ------------------------------------------------------- registry
class TestRegistryTab226:
    def test_tab226_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 260
        assert titoli[-1] == "❄️ Pompa di calore vs caldaia"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab226" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab226" in withs
        assert len(withs) == len(dvars) == 260
        keys = re.findall(r'key="(ai226_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
