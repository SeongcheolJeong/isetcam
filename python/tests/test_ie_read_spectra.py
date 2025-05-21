import unittest
import numpy as np
from pathlib import Path
from isetcam.ie_read_spectra import ie_read_spectra


class TestIeReadSpectra(unittest.TestCase):
    def test_basic(self):
        fname = Path('data/human/XYZ.mat')
        res, wave, comment, _ = ie_read_spectra(fname)
        self.assertEqual(res.shape[0], wave.shape[0])
        self.assertEqual(res.shape[1], 3)
        self.assertIsInstance(comment, str)

        wave2 = np.arange(400, 701, 10)
        res2, wave2_ret, _, _ = ie_read_spectra(fname, wave2)
        self.assertTrue(np.allclose(wave2, wave2_ret))
        self.assertEqual(res2.shape[0], len(wave2))


if __name__ == '__main__':
    unittest.main()
