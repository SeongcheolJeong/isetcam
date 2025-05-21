import numpy as np
import h5py


def read_hdf5(path_file):
    """Read hyperspectral data from an HDF5 file.

    Parameters
    ----------
    path_file : str or Path
        Path to the HDF5 file.

    Returns
    -------
    hymg : ndarray
        Reflectance datacube normalized between 0 and 1 with shape (H, W, N).
    color : ndarray
        RGB color image normalized between 0 and 1 with shape (H, W, 3).
    wave : ndarray
        Wavelength vector.
    """
    with h5py.File(path_file, "r") as f:
        keys = list(f.keys())
        if len(keys) < 3:
            raise ValueError("Expected at least three groups: color, reflectance, and wavelength")

        color_group = f[keys[0]]
        color_frames = [color_group[name][...] for name in color_group]
        color = np.stack([frame.T for frame in color_frames], axis=2) / 255.0

        refl_group = f[keys[1]]
        refl_frames = [refl_group[name][...] for name in refl_group]
        hymg = np.stack([frame.T for frame in refl_frames], axis=2) / 65536.0

        wave_group = f[keys[2]]
        wave_key = list(wave_group.keys())[0]
        wave = wave_group[wave_key][...]

    return hymg, color, wave
