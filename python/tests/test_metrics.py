import os
import sys
import unittest

# Add the parent directory to the Python path so that `isetcam` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from isetcam.metrics import exposure_value, iepsnr


class TestMetrics(unittest.TestCase):
    def test_exposure_value(self):
        ev = exposure_value(2.0, 0.5)
        expected = (2.0 ** 2) / 0.5
        expected = __import__('math').log2(expected)
        self.assertAlmostEqual(ev, expected)

    def test_exposure_value_errors(self):
        with self.assertRaises(ValueError):
            exposure_value(-1, 0.5)
        with self.assertRaises(ValueError):
            exposure_value(2, 0)

    def test_iepsnr_identical(self):
        img = [[0 for _ in range(10)] for _ in range(10)]
        self.assertEqual(iepsnr(img, img), float('inf'))

    def test_iepsnr_value(self):
        img1 = [[0 for _ in range(10)] for _ in range(10)]
        img2 = [[10 for _ in range(10)] for _ in range(10)]
        diff = 10
        mse = diff * diff
        expected = 20 * __import__('math').log10(255.0 / __import__('math').sqrt(mse))
        self.assertAlmostEqual(iepsnr(img1, img2), expected)

    def test_iepsnr_shape_error(self):
        img1 = [[0 for _ in range(5)] for _ in range(5)]
        img2 = [[0 for _ in range(4)] for _ in range(4)]
        with self.assertRaises(ValueError):
            iepsnr(img1, img2)


if __name__ == '__main__':
    unittest.main()
