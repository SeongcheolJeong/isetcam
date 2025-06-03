from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "display" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_display_introduction():
    mod = _load_tutorial("t_display_introduction.py")
    shape1, shape2, shape3 = mod.main()
    assert shape1 == shape2 == shape3
    assert len(shape1) == 3


def test_t_display_rendering():
    mod = _load_tutorial("t_display_rendering.py")
    patch = mod.main()
    assert patch.shape == (6, 4, 3)
