import unittest
import numpy as np
from ..ie_tone import ie_tone


class TestIeTone(unittest.TestCase):
    def test_tone_shape(self):
        fs = 1000
        duration = 0.1
        y = ie_tone(frequency=440, amplitude=0.5, duration=duration, fs=fs, play=False)
        expected_len = int(fs * duration) + 1
        self.assertEqual(len(y), expected_len)
        self.assertAlmostEqual(np.max(y), 0.5, places=2)


if __name__ == "__main__":
    unittest.main()
