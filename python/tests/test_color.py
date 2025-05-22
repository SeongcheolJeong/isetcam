import unittest
import numpy as np
from isetcam import quanta_to_energy, energy_to_quanta

class TestColorConversions(unittest.TestCase):
    def test_round_trip_vector(self):
        wave = np.arange(400, 710, 10)
        photons = np.linspace(1, 5, wave.size)
        energy = quanta_to_energy(wave, photons)
        recovered = energy_to_quanta(wave, energy)
        self.assertTrue(np.allclose(photons, recovered))

    def test_round_trip_image(self):
        wave = np.arange(400, 710, 10)
        data = np.random.rand(4, 5, wave.size)
        energy = quanta_to_energy(wave, data)
        recovered = energy_to_quanta(wave, energy)
        self.assertTrue(np.allclose(data, recovered))

if __name__ == '__main__':
    unittest.main()
