import sys
from pathlib import Path

# Make tools/build.py and tools/check_docs.py importable as top-level modules.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
