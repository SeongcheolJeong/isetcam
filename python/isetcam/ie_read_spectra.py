import numpy as np
from scipy.io import loadmat


def ie_read_spectra(fname, wave=None, extrap_val=0.0, make_positive=False):
    """Load spectral data from a .mat file and interpolate to desired wavelengths.

    Parameters
    ----------
    fname : str
        Path to the .mat file containing 'data' and 'wavelength' variables.
    wave : array-like, optional
        Desired wavelength samples. If None, the native wavelengths are used.
    extrap_val : float, optional
        Value used for extrapolation outside the wavelength range. Default 0.
    make_positive : bool, optional
        Ensure the first column has positive mean by flipping sign if needed.

    Returns
    -------
    res : ndarray
        Interpolated spectral data (len(wave) x nBands).
    wave : ndarray
        Wavelength samples used for interpolation.
    comment : str
        Comment field from the .mat file if present.
    fname : str
        Path to the loaded file (for reference).
    """
    if fname is None:
        raise ValueError("fname must be provided")

    mat = loadmat(fname)
    data = mat.get('data')
    wavelength = mat.get('wavelength')
    comment = mat.get('comment')
    if wavelength is None or data is None:
        raise ValueError(f"File {fname} missing required variables")

    wavelength = np.asarray(wavelength).squeeze()
    data = np.asarray(data)

    if wave is None:
        wave = wavelength
    else:
        wave = np.asarray(wave)

    if data.ndim == 1:
        res = np.interp(wave, wavelength, data, left=extrap_val, right=extrap_val)
    else:
        res = np.vstack([
            np.interp(wave, wavelength, data[:, i], left=extrap_val, right=extrap_val)
            for i in range(data.shape[1])
        ]).T

    if make_positive and res.ndim > 1 and np.mean(res[:, 0]) < 0:
        res = -res

    comment = str(comment.squeeze()) if comment is not None else ''

    return res, wave, comment, fname
