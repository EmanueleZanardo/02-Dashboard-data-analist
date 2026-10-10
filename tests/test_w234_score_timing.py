import re
from pathlib import Path
class TestRegistryTab234:
    def test_tab234_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 351
        assert "🎯 Score di timing" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab234" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab234" in withs
        assert len(withs) == len(dvars) == 351
        keys = re.findall(r'key="(t234_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
