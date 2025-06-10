# mypy: ignore-errors
"""Save a rendered RGB version of an OpticalImage."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import imageio.v2 as imageio

from .oi_class import OpticalImage
from ..display import Display, display_create, display_render, display_apply_gamma
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def _photons_to_rgb(oi: OpticalImage, display: Display) -> np.ndarray:
    photons = np.asarray(oi.photons, dtype=float)
    if photons.ndim != 3:
        raise ValueError("oi.photons must be a 3-D array")
    spd = np.asarray(display.spd, dtype=float)
    if photons.shape[2] != spd.shape[0]:
        raise ValueError("Wavelength dimension mismatch with display")

    xw, rows, cols = rgb_to_xw_format(photons)
    # ``spd`` is ``(n_wave, 3)``. Use the pseudoinverse of the transpose so the
    # multiplication yields ``(N, 3)`` RGB values.
    rgb_lin = xw @ np.linalg.pinv(spd.T)
    if display.gamma is not None:
        rgb = display_apply_gamma(rgb_lin, display, inverse=True)
    else:
        rgb = rgb_lin
    rgb = xw_to_rgb_format(rgb, rows, cols)
    return rgb


def oi_save_image(oi: OpticalImage, path: str | Path, display: Display | None = None) -> None:  # noqa: E501
    """Save an sRGB rendering of ``oi`` to ``path``."""
    if display is None:
        display = display_create()

    rgb = _photons_to_rgb(oi, display)
    spectral = display_render(rgb, display, apply_gamma=True)
    xyz = ie_xyz_from_photons(spectral, display.wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    arr = (np.clip(srgb, 0.0, 1.0) * 255).round().astype(np.uint8)
    imageio.imwrite(str(Path(path)), arr)
