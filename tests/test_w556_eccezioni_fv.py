"""Test tab556 'Fair value: eccezioni e approssimazioni (IFRS 7.29)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh556_num", "mh556_num_opt", "mh556_str", "mh556_motivo",
           "mh556_tipo", "mh556_classe", "mh556_demo", "mh556_riepilogo")

TITLE556 = "🏷️📋 Fair value: eccezioni e approssimazioni (IFRS 7.29)"


def _c(cid="C-1", d="x", tipo="CASSA", cv=1000000.0, fv=None,
       motivo="NESSUNA", mn=0.0, mx=0.0):
    return {"id": cid, "descrizione": d, "tipo": tipo,
            "valore_contabile": cv, "fair_value": fv, "motivo": motivo,
            "fv_min": mn, "fv_max": mx}


class TestW556Validatori:
    def test_num_ok(self):
        assert _F["mh556_num"](2, "x") == 2.0
        assert _F["mh556_num"](0, "x") == 0.0
        assert _F["mh556_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh556_num"](bad, "x")

    def test_num_opt_ok(self):
        assert _F["mh556_num_opt"](None, "x") is None
        assert _F["mh556_num_opt"](0, "x") == 0.0
        assert _F["mh556_num_opt"](3.25, "x") == 3.25

    def test_num_opt_ko(self):
        for bad in (True, False, "1", math.nan, math.inf, -1):
            with pytest.raises(ValueError):
                _F["mh556_num_opt"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh556_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh556_str"](bad, "x")

    def test_motivo_ok(self):
        for m in ("NESSUNA", "CV_APPROSSIMA_FV", "NON_MISURABILE",
                  "nessuna", " cv_approssima_fv "):
            assert _F["mh556_motivo"](m) in (
                "NESSUNA", "CV_APPROSSIMA_FV", "NON_MISURABILE")

    def test_motivo_ko(self):
        for bad in ("ALTRO", "", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh556_motivo"](bad)

    def test_tipo_ok_ko(self):
        for t in ("CASSA", "CREDITI_COMMERCIALI", "DEBITI_COMMERCIALI",
                  "DEPOSITI_CAUZIONALI", "PARTECIPAZIONE_NON_QUOTATA",
                  "STRUMENTO_LUNGO_TERMINE", "ALTRO"):
            assert _F["mh556_tipo"](t) == t
        for bad in ("BOND", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh556_tipo"](bad)

    def test_classe_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh556_classe"](["no"])


class TestW556Classe:
    def test_disclosure_ok(self):
        o = _F["mh556_classe"](_c(fv=990000.0))
        assert o["status"] == "DISCLOSURE_OK"
        assert o["anomalie"] == []
        assert abs(o["scostamento"] - (-0.01)) < 1e-12

    def test_esente_approssimazione(self):
        o = _F["mh556_classe"](_c(tipo="CASSA", motivo="CV_APPROSSIMA_FV"))
        assert o["status"] == "ESENTE_APPROSSIMAZIONE"
        assert o["anomalie"] == []
        assert o["scostamento"] is None

    def test_esente_non_misurabile(self):
        o = _F["mh556_classe"](_c(tipo="PARTECIPAZIONE_NON_QUOTATA",
                                 motivo="NON_MISURABILE", mn=800000.0,
                                 mx=1200000.0))
        assert o["status"] == "ESENTE_NON_MISURABILE"
        assert o["anomalie"] == []

    def test_anomalia_fv_mancante_senza_eccezione(self):
        o = _F["mh556_classe"](_c(fv=None, motivo="NESSUNA"))
        assert o["status"] == "DA_VERIFICARE"
        assert any("disclosure" in a for a in o["anomalie"])

    def test_anomalia_fv_con_non_misurabile(self):
        o = _F["mh556_classe"](_c(motivo="NON_MISURABILE", fv=1000000.0,
                                 mn=800000.0, mx=1200000.0))
        assert o["status"] == "DA_VERIFICARE"
        assert any("incoerenza" in a for a in o["anomalie"])

    def test_anomalia_range_non_valido(self):
        o = _F["mh556_classe"](_c(motivo="NON_MISURABILE", mn=1500000.0,
                                 mx=1200000.0))
        assert o["status"] == "DA_VERIFICARE"
        assert any("fv_min < fv_max" in a for a in o["anomalie"])

    def test_anomalia_cv_fuori_range(self):
        o = _F["mh556_classe"](_c(cv=2000000.0, motivo="NON_MISURABILE",
                                 mn=800000.0, mx=1200000.0))
        assert o["status"] == "DA_VERIFICARE"
        assert any("fuori dal range" in a for a in o["anomalie"])

    def test_anomalia_eccezione_a_su_lungo_termine(self):
        o = _F["mh556_classe"](_c(tipo="STRUMENTO_LUNGO_TERMINE",
                                 motivo="CV_APPROSSIMA_FV"))
        assert o["status"] == "DA_VERIFICARE"
        assert any("breve termine" in a for a in o["anomalie"])

    def test_scostamento_oltre_soglia(self):
        # FV disclosato con 7.29(a) ma scostamento -10% > soglia 5%
        r = _F["mh556_riepilogo"]([_c(motivo="CV_APPROSSIMA_FV",
                                     fv=900000.0)],
                                  soglia_scostamento=0.05)
        o = r["classi"][0]
        assert o["status"] == "DA_VERIFICARE"
        assert any("non e' credibile" in a for a in o["anomalie"])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_scostamento_entro_soglia(self):
        r = _F["mh556_riepilogo"]([_c(motivo="CV_APPROSSIMA_FV",
                                     fv=990000.0)],
                                  soglia_scostamento=0.05)
        o = r["classi"][0]
        assert o["status"] == "ESENTE_APPROSSIMAZIONE"
        assert o["anomalie"] == []
        assert r["verdetto"] == "ESENZIONI_DOCUMENTATE"


class TestW556Riepilogo:
    def test_demo_esenzioni_documentate(self):
        r = _F["mh556_riepilogo"](_F["mh556_demo"]())
        assert r["n_classi"] == 3
        assert r["valore_contabile_tot"] == pytest.approx(11800000.0)
        assert r["fair_value_tot"] == pytest.approx(8150000.0)
        assert r["n_esenti"] == 2
        assert r["n_anomalie"] == 0
        assert r["verdetto"] == "ESENZIONI_DOCUMENTATE"
        stati = [o["status"] for o in r["classi"]]
        assert stati == ["ESENTE_APPROSSIMAZIONE", "DISCLOSURE_OK",
                         "ESENTE_NON_MISURABILE"]

    def test_verdetto_informativa_completa(self):
        r = _F["mh556_riepilogo"]([_c(fv=990000.0),
                                  _c(cid="C-2", fv=500000.0)])
        assert r["verdetto"] == "INFORMATIVA_COMPLETA"

    def test_verdetto_nessuna_classe(self):
        r = _F["mh556_riepilogo"]([_c(cv=0.0, fv=None,
                                     motivo="CV_APPROSSIMA_FV")])
        assert r["verdetto"] == "NESSUNA_CLASSE"

    def test_verdetto_anomalie(self):
        r = _F["mh556_riepilogo"]([_c(fv=None, motivo="NESSUNA")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh556_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh556_riepilogo"]("no")

    def test_soglie_degeneri(self):
        for bad in (True, "0.05", math.nan, math.inf, 0.0, -0.1, 1.5):
            with pytest.raises(ValueError):
                _F["mh556_riepilogo"]([_c(fv=1.0)],
                                      soglia_scostamento=bad)

    def test_soglia_personalizzata(self):
        # scostamento -10%: con soglia 15% resta esente
        r = _F["mh556_riepilogo"]([_c(motivo="CV_APPROSSIMA_FV",
                                     fv=900000.0)],
                                  soglia_scostamento=0.15)
        assert r["verdetto"] == "ESENZIONI_DOCUMENTATE"


class TestW556Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_556_presente(self):
        assert self._src().count(TITLE556) == 3

    def test_counts_556(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 690
        assert TITLE556 in titoli
        assert "tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690 = st.tabs([" in src

    def test_chiavi_556_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st556_" in ln]
        # le f-string st556_id_{_i556} generano istanze a runtime: la base
        # e' fino al suffisso numerico; run/csv1/csv2 sono chiavi distinte
        basi = []
        for ln in righe:
            basi.append(re.search(r"st556_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 13
