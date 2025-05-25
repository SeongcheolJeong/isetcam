"""Color space transformation utilities in Python.

This module provides simple conversions between linear RGB (lrgb)
and nonlinear sRGB values used in ISETCam.
"""

import numpy as np


def lrgb2srgb(rgb: np.ndarray) -> np.ndarray:
    """Convert linear RGB values to standard sRGB.

    Parameters
    ----------
    rgb : ndarray
        Linear RGB values in the range [0, 1].

    Returns
    -------
    ndarray
        Nonlinear sRGB values in the range [0, 1].
    """
    if rgb.min() < 0 or rgb.max() > 1:
        raise ValueError("Linear rgb values must be between 0 and 1")

    rgb = rgb.copy()
    mask = rgb > 0.0031308
    rgb[~mask] *= 12.92
    rgb[mask] = 1.055 * np.power(rgb[mask], 1 / 2.4) - 0.055
    return rgb


def srgb2lrgb(rgb: np.ndarray) -> np.ndarray:
    """Convert nonlinear sRGB values to linear RGB.

    Parameters
    ----------
    rgb : ndarray
        Nonlinear sRGB values in the range [0, 1].

    Returns
    -------
    ndarray
        Linear RGB values in the range [0, 1].
    """
    if rgb.max() > 1 or rgb.min() < 0:
        raise ValueError("sRGB values must be between 0 and 1")

    rgb = rgb.copy()
    mask = rgb > 0.04045
    rgb[~mask] /= 12.92
    rgb[mask] = np.power((rgb[mask] + 0.055) / 1.055, 2.4)
    return rgb
