import os
import unittest
import numpy as np
import tempfile

try:
    import h5py
    from utility.hypercube.read_hdf5 import read_hdf5
except Exception:  # pragma: no cover
    h5py = None


class TestReadHDF5(unittest.TestCase):
    @unittest.skipUnless(h5py is not None, "h5py not installed")
    def test_read_hdf5(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.h5")
            with h5py.File(path, "w") as f:
                color = f.create_group("ColorImage")
                color.create_dataset("R", data=np.ones((2, 3)) * 255)
                color.create_dataset("G", data=np.ones((2, 3)) * 128)
                color.create_dataset("B", data=np.ones((2, 3)) * 64)

                refl = f.create_group("Hymage")
                for i in range(4):
                    refl.create_dataset(str(i), data=np.full((2, 3), i * 1000))

                wave = f.create_group("Wavelength")
                wave.create_dataset("wave", data=np.array([450, 550, 650, 750]))

            hymg, color_img, wave = read_hdf5(path)
            self.assertEqual(color_img.shape, (3, 2, 3))
            self.assertEqual(hymg.shape, (3, 2, 4))
            self.assertEqual(wave.shape[0], 4)


if __name__ == "__main__":
    unittest.main()
