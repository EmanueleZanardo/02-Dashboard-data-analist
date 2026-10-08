"""Test tab213 'Rinnovo vs switch fornitore': helper calcola_confronto_offerte —
TCO annuo di offerte di fornitura (rinnovo vs alternative), all-in EUR/MWh,
volumi di pareggio tra coppie di offerte.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("calcola_confronto_offerte")
calcola_confronto_offerte = _F["calcola_confronto_offerte"]

APP = Path(__file__).parent.parent / "app.py"

# V = 1000 MWh/anno
RINNOVO = dict(nome="Rinnovo (attuale)", prezzo_energia_eur_mwh=120.0,
               canone_fisso_eur_mese=50.0, durata_mesi=12,
               costo_attivazione_eur=0.0, sconto_pct=0.0)
ALT_A = dict(nome="Alternativa A", prezzo_energia_eur_mwh=100.0,
             canone_fisso_eur_mese=200.0, durata_mesi=12,
             costo_attivazione_eur=500.0, sconto_pct=0.0)
ALT_B = dict(nome="Alternativa B", prezzo_energia_eur_mwh=110.0,
             canone_fisso_eur_mese=30.0, durata_mesi=12,
             costo_attivazione_eur=0.0, sconto_pct=5.0)


class TestNumeriAMano:
    def test_tco_e_allin(self):
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        assert r["errore"] is None and r["valido"] is True
        df = r["df"]
        assert list(df["Offerta"]) == ["Rinnovo (attuale)", "Alternativa A",
                                       "Alternativa B"]
        # Rinnovo: 1000*120 + 12*50 + 0 = 120600
        assert df["TCO annuo (€)"].iloc[0] == pytest.approx(120600.0)
        assert df["All-in (€/MWh)"].iloc[0] == pytest.approx(120.60)
        # Alt A: 1000*100 + 12*200 + 500 = 102900
        assert df["TCO annuo (€)"].iloc[1] == pytest.approx(102900.0)
        assert df["All-in (€/MWh)"].iloc[1] == pytest.approx(102.90)
        # Alt B: prezzo eff. 104.5 -> 1000*104.5 + 12*30 = 104860
        assert df["Prezzo eff. (€/MWh)"].iloc[2] == pytest.approx(104.50)
        assert df["TCO annuo (€)"].iloc[2] == pytest.approx(104860.0)
        assert df["All-in (€/MWh)"].iloc[2] == pytest.approx(104.86)

    def test_verdetto_e_risparmio(self):
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        assert r["verdetto"] == "CONVIENE LO SWITCH"
        assert r["migliore"] == "Alternativa A"
        assert r["tco_migliore"] == pytest.approx(102900.0)
        assert r["allin_migliore"] == pytest.approx(102.90)
        assert r["tco_rinnovo"] == pytest.approx(120600.0)
        # 120600 - 102900 = 17700
        assert r["risparmio_vs_rinnovo"] == pytest.approx(17700.0)

    def test_verdetto_resta_quando_rinnovo_migliore(self):
        caro = dict(ALT_A, nome="Cara")
        caro = dict(caro, prezzo_energia_eur_mwh=200.0)
        r = calcola_confronto_offerte([RINNOVO, caro], 1000.0)
        assert r["verdetto"] == "RESTA NEL CONTRATTO"
        assert r["migliore"] == "Rinnovo (attuale)"
        assert r["risparmio_vs_rinnovo"] == pytest.approx(0.0)

    def test_verdetto_indifferente(self):
        gemella = dict(RINNOVO, nome="Gemella")
        r = calcola_confronto_offerte([RINNOVO, gemella], 1000.0)
        assert r["verdetto"] == "INDIFFERENTE"
        assert r["risparmio_vs_rinnovo"] == pytest.approx(0.0)


class TestVolumiPareggio:
    def test_pareggio_rinnovo_vs_alta(self):
        # a = 120-100 = 20; num = 12*(200-50) + 500 = 2300; V* = 115
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        dp = r["df_pareggi"]
        riga = dp[dp["Coppia"] == "Rinnovo (attuale) vs Alternativa A"].iloc[0]
        assert riga["Volume pareggio (MWh/anno)"] == pytest.approx(115.0)
        assert "Rinnovo (attuale)" in riga["Lettura"]
        assert "Alternativa A" in riga["Lettura"]
        assert "Fino a 115" in riga["Lettura"]

    def test_nessun_incrocio(self):
        # Rinnovo vs B: V* = -240/15.5 < 0 -> B sempre piu' economica
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        dp = r["df_pareggi"]
        riga = dp[dp["Coppia"] == "Rinnovo (attuale) vs Alternativa B"].iloc[0]
        assert riga["Volume pareggio (MWh/anno)"] is None or \
            str(riga["Volume pareggio (MWh/anno)"]) in ("None", "nan")
        assert "sempre piu' economica" in riga["Lettura"]
        assert "Alternativa B" in riga["Lettura"]

    def test_pareggio_a_vs_b(self):
        # a = 100-104.5 = -4.5; num = 12*(30-200) - 500 = -2540
        # V* = 2540/4.5 = 564.44...
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        dp = r["df_pareggi"]
        riga = dp[dp["Coppia"] == "Alternativa A vs Alternativa B"].iloc[0]
        assert riga["Volume pareggio (MWh/anno)"] == pytest.approx(564.0,
                                                                  abs=1.0)
        # a basso volume vince B (fissi minori), sopra vince A
        assert "Alternativa B" in riga["Lettura"]
        assert "Alternativa A" in riga["Lettura"]

    def test_pareggio_coerente_con_tco(self):
        # Al volume di pareggio A vs B i due TCO devono coincidere
        r = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        dp = r["df_pareggi"]
        vstar = dp[dp["Coppia"] == "Alternativa A vs Alternativa B"] \
            ["Volume pareggio (MWh/anno)"].iloc[0]
        r2 = calcola_confronto_offerte([ALT_A, ALT_B], float(vstar))
        t = r2["tco"]
        assert abs(t[0] - t[1]) / max(t) < 0.002


class TestErrori:
    def test_meno_di_due_offerte(self):
        r = calcola_confronto_offerte([RINNOVO], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_volume_zero(self):
        r = calcola_confronto_offerte([RINNOVO, ALT_A], 0.0)
        assert r["errore"] and not r["valido"]

    def test_volume_non_numerico(self):
        r = calcola_confronto_offerte([RINNOVO, ALT_A], "tanto")
        assert r["errore"] and not r["valido"]

    def test_prezzo_negativo(self):
        o = dict(ALT_A, prezzo_energia_eur_mwh=-5.0)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_canone_negativo(self):
        o = dict(ALT_A, canone_fisso_eur_mese=-1.0)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_attivazione_negativa(self):
        o = dict(ALT_A, costo_attivazione_eur=-10.0)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_sconto_oltre_100(self):
        o = dict(ALT_B, sconto_pct=120.0)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_durata_non_intera(self):
        o = dict(ALT_A, durata_mesi=12.5)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_durata_fuori_range(self):
        o = dict(ALT_A, durata_mesi=200)
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_parametro_mancante(self):
        o = dict(ALT_A)
        del o["prezzo_energia_eur_mwh"]
        r = calcola_confronto_offerte([RINNOVO, o], 1000.0)
        assert r["errore"] and not r["valido"]

    def test_offerta_non_dict(self):
        r = calcola_confronto_offerte([RINNOVO, "offerta"], 1000.0)
        assert r["errore"] and not r["valido"]


class TestDeterminismo:
    def test_due_run_identici(self):
        r1 = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        r2 = calcola_confronto_offerte([RINNOVO, ALT_A, ALT_B], 1000.0)
        assert r1["df"].equals(r2["df"])
        assert r1["df_pareggi"].equals(r2["df_pareggi"])
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["tco"] == r2["tco"]


class TestRegistry:
    def test_tab213_dichiarata(self):
        import ast as _ast
        src = APP.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        titoli = None
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Assign)
                    and isinstance(node.value, _ast.Call)
                    and getattr(getattr(node.value.func, "attr", ""),
                                "lower", lambda: "")() == "tabs"
                                and node.value.args and hasattr(node.value.args[0], "elts")):
                titoli = [t.value for t in node.value.args[0].elts]
        assert titoli is not None
        assert len(titoli) == 301
        assert titoli[-1] == "🛡️🔍 Rischio di modello: quale VaR credere?"
        # variabili tabN: devono essere 217 e tab216 presente (non più ultima)
        m = re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 301
        assert "tab212" in vars_tab and "tab213" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 301
        assert "tab213" in withs and "tab214" in withs
        # key widget uniche: 2 letterali + 5 template f-string (x3 offerte)
        keys = re.findall(r'key=f?"(cfo213_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 7
        assert '"rin"' in src and '"altA"' in src and '"altB"' in src
