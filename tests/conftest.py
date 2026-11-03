import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for folder in (ROOT / "src" / "vault-keeper", ROOT / "heist"):
    sys.path.insert(0, str(folder))
