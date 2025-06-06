import numpy as np
from pathlib import Path
from scipy.io import loadmat

from isetcam import data_path

from isetcam import scotopic_luminance_from_energy


def _expected_scotopic_luminance(wave, energy):
    mat = loadmat(data_path('human/rods.mat'))
    Vp = np.interp(wave, mat['wavelength'].ravel(), mat['data'].ravel(), left=0.0, right=0.0)
    binwidth = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    lum = 1745 * xw.dot(Vp) * binwidth
    return lum.reshape(energy.shape[:-1])


def test_scotopic_luminance_from_energy_xw():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    lum = scotopic_luminance_from_energy(energy, wave)
    expected = _expected_scotopic_luminance(wave, energy)
    assert np.allclose(lum, expected)


def test_scotopic_luminance_from_energy_rgb():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, 1, len(wave)))
    lum = scotopic_luminance_from_energy(energy, wave)
    expected = _expected_scotopic_luminance(wave, energy.reshape(1, len(wave)))
    assert np.allclose(lum, expected.reshape(1, 1))
