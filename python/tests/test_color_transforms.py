import numpy as np
import sys
from pathlib import Path

# Ensure the parent directory is on the path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from color_transforms import lrgb2srgb, srgb2lrgb


def test_roundtrip():
    rng = np.random.RandomState(0)
    data = rng.rand(10, 3)
    converted = lrgb2srgb(data)
    reverted = srgb2lrgb(converted)
    assert np.allclose(data, reverted, atol=1e-6)
