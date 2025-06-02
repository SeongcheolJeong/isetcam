import numpy as np

from isetcam.scene import scene_from_basis, Scene
from isetcam.illuminant import Illuminant


def test_scene_from_basis():
    wave = np.array([1.0, 2.0, 3.0], dtype=float)
    basis_mat = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
    mc = np.array([[[1, 2]], [[3, 4]]], dtype=float)
    img_mean = np.array([0.5, 1.0, 1.5], dtype=float)
    illum = Illuminant(spd=np.array([10, 20, 30], dtype=float), wave=wave, name="test")

    sceneS = {
        "mcCOEF": mc,
        "basis": {"basis": basis_mat, "wave": wave},
        "imgMean": img_mean,
        "illuminant": illum,
    }

    sc = scene_from_basis(sceneS)
    assert isinstance(sc, Scene)
    expected = mc.reshape(-1, mc.shape[-1]) @ basis_mat.T
    expected = expected.reshape(mc.shape[0], mc.shape[1], wave.size) + img_mean.reshape(1, 1, -1)
    assert np.allclose(sc.photons, expected)
    assert np.array_equal(sc.wave, wave)
    assert isinstance(getattr(sc, "illuminant", None), Illuminant)
    assert np.array_equal(sc.illuminant.spd, illum.spd)
