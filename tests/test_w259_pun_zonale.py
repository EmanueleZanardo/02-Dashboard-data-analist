"""Test tab259 'PUN da prezzi zonali': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab259.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pun259_num", "pun259_zone", "pun259_pesi_default",
          "pun259_normalizza_pesi", "pun259_parsa_prezzi",
          "pun259_pun_orario", "pun259_spread_zonali", "pun259_sintesi")
pun259_num = _F["pun259_num"]
pun259_zone = _F["pun259_zone"]
pun259_pesi_default = _F["pun259_pesi_default"]
pun259_normalizza_pesi = _F["pun259_normalizza_pesi"]
pun259_parsa_prezzi = _F["pun259_parsa_prezzi"]
pun259_pun_orario = _F["pun259_pun_orario"]
pun259_spread_zonali = _F["pun259_spread_zonali"]
pun259_sintesi = _F["pun259_sintesi"]

APP = Path(__file__).parent.parent / "app.py"

PREZZI = {"NORD": 100.0, "CNOR": 90.0, "CSUD": 80.0,
          "SUD": 70.0, "SICI": 60.0, "SARD": 50.0}
# PUN atteso con pesi default: .46*100+.17*90+.12*80+.08*70+.07*60+.10*50 = 85.7
PUN_ATTESO = 85.7


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab259:
    def test_tab259_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 349
        assert "🇮🇹 PUN da prezzi zonali" in titoli
        assert "tab259" in dvars
        assert "tab259" in withs
        assert titoli[dvars.index("tab259")] == "🇮🇹 PUN da prezzi zonali"
        assert titoli[-1] == "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
        keys = re.findall(r'key="(pun259_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_258_259(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab258")] == "🌿 Clean spread (con CO₂)"
        assert titoli[dvars.index("tab259")] == "🇮🇹 PUN da prezzi zonali"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("pun259_num", "pun259_zone", "pun259_pesi_default",
                   "pun259_normalizza_pesi", "pun259_parsa_prezzi",
                   "pun259_pun_orario", "pun259_spread_zonali", "pun259_sintesi"):
            assert src.index(f"def {fn}(") < i_ws


class TestPun259Num:
    def test_ok(self):
        assert pun259_num(3, "x") == 3.0
        assert pun259_num(-2.5, "x") == -2.5

    def test_errori(self):
        for bad in (True, False, "3", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                pun259_num(bad, "x")


class TestPun259Pesi:
    def test_zone(self):
        assert pun259_zone() == ["NORD", "CNOR", "CSUD", "SUD", "SICI", "SARD"]

    def test_default(self):
        p = pun259_pesi_default()
        assert set(p) == set(pun259_zone())
        assert sum(p.values()) == pytest.approx(1.0)

    def test_normalizza(self):
        out = pun259_normalizza_pesi({z: 1.0 for z in pun259_zone()})
        assert all(v == pytest.approx(1 / 6) for v in out.values())
        assert sum(out.values()) == pytest.approx(1.0)
        out2 = pun259_normalizza_pesi({**pun259_pesi_default(), "NORD": 0.90})
        assert out2["NORD"] == pytest.approx(0.90 / 1.44)

    def test_errori(self):
        with pytest.raises(ValueError):
            pun259_normalizza_pesi({"NORD": 1.0})
        with pytest.raises(ValueError):
            pun259_normalizza_pesi({z: (-1.0 if z == "NORD" else 0.1)
                                    for z in pun259_zone()})
        with pytest.raises(ValueError):
            pun259_normalizza_pesi({z: 0.0 for z in pun259_zone()})
        with pytest.raises(ValueError):
            pun259_normalizza_pesi([1, 2, 3])


class TestPun259Parsa:
    def test_base(self):
        righe = pun259_parsa_prezzi("00;100;90;80;70;60;50\n01;80;80;80;80;80;80")
        assert len(righe) == 2
        assert righe[0]["ora"] == "00"
        assert righe[0]["NORD"] == 100.0
        assert righe[1]["SARD"] == 80.0

    def test_virgola_e_intestazione_e_vuoti(self):
        txt = "ora,NORD,CNOR,CSUD,SUD,SICI,SARD\n\n00,100,90,80,70,60,50\n"
        righe = pun259_parsa_prezzi(txt)
        assert len(righe) == 1
        assert righe[0]["CNOR"] == 90.0

    def test_negativi_ok(self):
        righe = pun259_parsa_prezzi("00;-5;90;80;70;60;50")
        assert righe[0]["NORD"] == -5.0

    def test_errori(self):
        with pytest.raises(ValueError):
            pun259_parsa_prezzi("")
        with pytest.raises(ValueError):
            pun259_parsa_prezzi("00;100;90;80;70;60")
        with pytest.raises(ValueError):
            pun259_parsa_prezzi("00;100;xx;80;70;60;50")


class TestPun259PunOrario:
    def test_pun(self):
        o = pun259_pun_orario(PREZZI, pun259_pesi_default())
        assert o["pun"] == pytest.approx(PUN_ATTESO)
        assert o["zona_min"] == "SARD"
        assert o["zona_max"] == "NORD"
        assert o["prezzo_min"] == 50.0
        assert o["prezzo_max"] == 100.0
        assert o["spread_max_min"] == pytest.approx(50.0)

    def test_pesi_non_normalizzati(self):
        o = pun259_pun_orario(PREZZI, {z: 2.0 for z in pun259_zone()})
        assert o["pun"] == pytest.approx(sum(PREZZI.values()) / 6)

    def test_errore_zona_mancante(self):
        with pytest.raises(ValueError):
            pun259_pun_orario({"NORD": 100.0}, pun259_pesi_default())


class TestPun259SpreadZonali:
    def test_spread(self):
        s = pun259_spread_zonali(PUN_ATTESO, PREZZI)
        assert s["NORD"] == pytest.approx(14.3)
        assert s["CNOR"] == pytest.approx(4.3)
        assert s["CSUD"] == pytest.approx(-5.7)
        assert s["SUD"] == pytest.approx(-15.7)
        assert s["SICI"] == pytest.approx(-25.7)
        assert s["SARD"] == pytest.approx(-35.7)
        # somma pesata degli spread e' zero per costruzione
        pw = pun259_pesi_default()
        assert sum(pw[z] * s[z] for z in pw) == pytest.approx(0.0)

    def test_errore(self):
        with pytest.raises(ValueError):
            pun259_spread_zonali("x", PREZZI)


class TestPun259Sintesi:
    def _righe(self):
        o1 = pun259_pun_orario(PREZZI, pun259_pesi_default())
        prezzi2 = {z: v - 10 for z, v in PREZZI.items()}
        o2 = pun259_pun_orario(prezzi2, pun259_pesi_default())
        return [
            {"ora": "18", "pun": o1["pun"],
             "spread_max_min": o1["spread_max_min"], **PREZZI},
            {"ora": "19", "pun": o2["pun"],
             "spread_max_min": o2["spread_max_min"], **prezzi2},
        ]

    def test_sintesi(self):
        sin = pun259_sintesi(self._righe())
        assert sin["n_ore"] == 2
        assert sin["pun_medio"] == pytest.approx(PUN_ATTESO - 5.0)
        assert sin["pun_max"] == pytest.approx(PUN_ATTESO)
        assert sin["ora_max"] == "18"
        assert sin["pun_min"] == pytest.approx(PUN_ATTESO - 10.0)
        assert sin["ora_min"] == "19"
        assert sin["spread_max_min_medio"] == pytest.approx(50.0)
        assert sin["zona_piu_cara"] == "NORD"
        assert sin["zona_piu_economica"] == "SARD"
        assert sin["prezzo_medio_zona"]["NORD"] == pytest.approx(95.0)
        assert sin["spread_medio_zona_vs_pun"]["NORD"] == pytest.approx(14.3)
        assert sin["ore_congestione"] == 2

    def test_soglia(self):
        sin = pun259_sintesi(self._righe(), soglia_congestione=60.0)
        assert sin["ore_congestione"] == 0

    def test_errori(self):
        with pytest.raises(ValueError):
            pun259_sintesi([])
        with pytest.raises(ValueError):
            pun259_sintesi(self._righe(), soglia_congestione=-1.0)
        righe = self._righe()
        del righe[0]["SARD"]
        with pytest.raises(ValueError):
            pun259_sintesi(righe)
