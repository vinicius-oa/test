import sys
from pathlib import Path

# set `src` dir in `PYTHONPATH`
backend_dir = Path(__file__).parent.parent
src_path = backend_dir.joinpath("/".join((str(backend_dir), "app")))
sys.path.append(str(src_path))
