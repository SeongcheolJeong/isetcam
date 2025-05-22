import numpy as np

# Mapping of physical constants used in ISETCam
VC_CONSTANTS = {
    'planck': 6.626176e-34,
    'h': 6.626176e-34,
    'plancksconstant': 6.626176e-34,
    'q': 1.602177e-19,
    'electroncharge': 1.602177e-19,
    'c': 2.99792458e8,
    'speedoflight': 2.99792458e8,
    'j': 1.380662e-23,
    'joulesperkelvin': 1.380662e-23,
    'boltzman': 1.380662e-23,
    'mmperdeg': 0.3,
}


def vc_constants(key: str) -> float:
    """Return the value of a physical constant.

    Parameters
    ----------
    key : str
        Name of the constant. The lookup is case-insensitive and
        follows the names used in the MATLAB ``vcConstants`` function.

    Returns
    -------
    float
        Numerical value of the constant.
    """
    k = key.lower()
    if k not in VC_CONSTANTS:
        raise ValueError(f"Unknown physical constant: {key}")
    return VC_CONSTANTS[k]


def rgb2xw(image: np.ndarray):
    """Convert an array from RGB (row, col, wave) format to XW format.

    Parameters
    ----------
    image : ndarray
        Array in (rows, cols, wavelengths) format. If the input is a
        2-D array it is treated as having a single wavelength.

    Returns
    -------
    xw : ndarray
        Array of shape (rows*cols, wavelengths).
    r : int
        Number of rows in the input image.
    c : int
        Number of columns in the input image.
    w : int
        Number of wavelength bands.
    """
    arr = np.asarray(image)
    if arr.ndim == 2:
        arr = arr[:, :, None]
    r, c, w = arr.shape
    xw = arr.reshape((r * c, w))
    return xw, r, c, w


def xw2rgb(xw: np.ndarray, r: int, c: int) -> np.ndarray:
    """Convert an array from XW format back to RGB format."""
    xw = np.asarray(xw)
    w = xw.shape[1]
    if xw.shape[0] != r * c:
        raise ValueError('row*col must equal number of rows in xw')
    return xw.reshape((r, c, w))


def quanta_to_energy(wavelength, photons):
    """Convert quanta (photons) to energy.

    Parameters
    ----------
    wavelength : array_like
        Sample wavelengths in nanometers.
    photons : ndarray
        Spectral data either in RGB (rows, cols, wave) or XW format.

    Returns
    -------
    ndarray
        Energy in the same format as the input.
    """
    wave = np.asarray(wavelength).reshape(-1)
    p = np.asarray(photons)
    h = vc_constants('h')
    c = vc_constants('c')

    if p.ndim == 3:
        xw, r, c_, _ = rgb2xw(p)
        energy = (h * c / 1e-9) * (xw / wave)
        energy = xw2rgb(energy, r, c_)
    else:
        if p.ndim == 1:
            p = p[np.newaxis, :]
        if p.shape[1] != wave.size:
            raise ValueError('photons must have columns equal to number of wavelengths')
        energy = (h * c / 1e-9) * (p / wave)
        if energy.shape[0] == 1:
            energy = energy[0]
    return energy


def energy_to_quanta(wavelength, energy):
    """Convert energy to number of photons."""
    wave = np.asarray(wavelength).reshape(-1)
    e = np.asarray(energy)
    h = vc_constants('h')
    c = vc_constants('c')

    if e.ndim == 3:
        n, m, w = e.shape
        if w != wave.size:
            raise ValueError('energy third dimension must equal number of wavelengths')
        reshaped = e.reshape((n * m, w)).T
        photons = (reshaped / (h * c)) * (1e-9 * wave[:, None])
        photons = photons.T.reshape((n, m, w))
    else:
        if e.ndim == 1:
            e = e[:, np.newaxis]
        if e.shape[0] != wave.size:
            raise ValueError('energy rows must equal number of wavelengths')
        photons = (e / (h * c)) * (1e-9 * wave[:, None])
        if photons.shape[1] == 1:
            photons = photons[:, 0]
    return photons
