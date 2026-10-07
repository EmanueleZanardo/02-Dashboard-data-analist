"""Configurazione pytest per tests/.

I file legacy in stile "QA standalone" (test_*_<data>_<ora>.py e
test_helpers.py) eseguono i check all'import e terminano con SystemExit:
non sono collezionabili da pytest e vengono ignorati qui. Restano
eseguibili direttamente con `python3 tests/<file>.py` oppure tutti insieme
con `python3 tests/run_all.py`.
"""

from pathlib import Path
import os

_DIR = Path(__file__).parent
_REPO_ROOT = _DIR.parent

# Robustezza: 34 file di test aprono "app.py" con path relativo alla cwd.
# Se pytest viene lanciato da una directory diversa dalla root del repo,
# la collection fallirebbe con FileNotFoundError. Forziamo la cwd sulla
# root del repo all'import di conftest (no-op se gia' corretta).
try:
    os.chdir(_REPO_ROOT)
except OSError:
    pass


def _is_legacy_standalone(path: Path) -> bool:
    try:
        src = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return "raise SystemExit" in src or "\nsys.exit(" in src


collect_ignore = sorted(
    p.name for p in _DIR.glob("test_*.py") if _is_legacy_standalone(p)
)
