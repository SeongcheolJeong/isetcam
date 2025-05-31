"""Utility functions for reading and writing ISETCam color filter files.

These helpers mirror the behavior of the MATLAB functions
`ieReadColorFilter` and `ieSaveColorFilter`.
"""

from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import Iterable, Dict, Any, Optional, Tuple

from scipy.io import loadmat, savemat

__all__ = ["read_color_filter", "save_color_filter"]


def read_color_filter(
    file_path: str | Path, wave: Optional[Iterable[float]] = None
) -> Tuple[np.ndarray, np.ndarray, Iterable[str], Dict[str, Any]]:
    """Read a color filter definition from a ``.mat`` file.

    Parameters
    ----------
    file_path: str or Path
        Path to the ``.mat`` file created by ``ieSaveColorFilter``.
    wave: iterable of float, optional
        Desired wavelength samples. If provided, the returned data are
        interpolated to these wavelengths.

    Returns
    -------
    wavelengths : numpy.ndarray
        Wavelength samples from the file or the requested ``wave``.
    data : numpy.ndarray
        Filter transmissivity spectra arranged in columns.
    filter_names : list of str
        Names of the filters.
    all_fields : dict
        All fields loaded from the ``.mat`` file.
    """

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Missing color filter file: {file_path}")

    mat = loadmat(file_path.as_posix())

    # MATLAB stores cell arrays as object arrays. Convert to a Python list of
    # strings.
    filter_field = mat.get("filterNames")
    if filter_field is None:
        filter_names = []
    else:
        filter_names = [str(x.item()) for x in np.ravel(filter_field)]
    wavelengths = mat.get("wavelength")
    data = mat.get("data")

    if wavelengths is None or data is None:
        raise ValueError("Color filter file missing required fields")

    wavelengths = np.asarray(wavelengths).squeeze()
    data = np.asarray(data)

    if wave is not None:
        wave = np.asarray(list(wave))
        data = np.interp(wave, wavelengths, data, left=0, right=0)
        wavelengths = wave

    return wavelengths, data, filter_names, mat


def save_color_filter(
    file_path: str | Path,
    wavelengths: Iterable[float],
    data: np.ndarray,
    filter_names: Iterable[str],
    comment: str | None = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> None:
    """Write a color filter definition to a ``.mat`` file.

    Parameters
    ----------
    file_path: str or Path
        Destination path.
    wavelengths: iterable
        Wavelength samples.
    data: numpy.ndarray
        Filter transmissivity spectra.
    filter_names: iterable of str
        Names of the filters.
    comment: str, optional
        Comment stored in the file.
    extra_fields: dict, optional
        Additional fields stored in the file.
    """

    file_path = Path(file_path)
    wavelengths = np.asarray(list(wavelengths))
    data = np.asarray(data)
    filter_names = list(filter_names)

    mdict = {
        "wavelength": wavelengths,
        "data": data,
        "filterNames": np.array(filter_names, dtype=object),
    }
    if comment is not None:
        mdict["comment"] = comment
    if extra_fields:
        mdict.update(extra_fields)

    savemat(file_path.as_posix(), mdict, do_compression=False)
