# mypy: ignore-errors
"""Display an OpticalImage using Matplotlib."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .oi_class import OpticalImage
from ..display import Display, display_create, display_render, display_apply_gamma
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb
from ..ie_format_figure import ie_format_figure


def _photons_to_rgb(oi: OpticalImage, display: Display) -> np.ndarray:
    """Convert optical image photons to display RGB values."""
    photons = np.asarray(oi.photons, dtype=float)
    if photons.ndim != 3:
        raise ValueError("oi.photons must be a 3-D array")
    spd = np.asarray(display.spd, dtype=float)
    if photons.shape[2] != spd.shape[0]:
        raise ValueError("Wavelength dimension mismatch with display")

    xw, rows, cols = rgb_to_xw_format(photons)
    # Solve for the display RGB values that reproduce the spectral data.
    # ``spd`` has shape ``(n_wave, 3)`` so we need the pseudoinverse of its
    # transpose to obtain a ``(n_wave, 3)`` -> ``(3,)`` mapping.
    rgb_lin = xw @ np.linalg.pinv(spd.T)
    if display.gamma is not None:
        rgb = display_apply_gamma(rgb_lin, display, inverse=True)
    else:
        rgb = rgb_lin
    rgb = xw_to_rgb_format(rgb, rows, cols)
    return rgb


def oi_show_image(oi: OpticalImage, display: Display | None = None):
    """Render ``oi`` to RGB for ``display`` and show with matplotlib."""
    if plt is None:
        raise ImportError("matplotlib is required for oi_show_image")
    if display is None:
        display = display_create()

    rgb = _photons_to_rgb(oi, display)
    # Render through the display model
    spectral = display_render(rgb, display, apply_gamma=True)
    if spectral.shape[-1] != len(display.wave):
        raise ValueError(
            "display.spd must be resampled to display.wave; expected"
            f" {len(display.wave)}, got {spectral.shape[-1]}"
        )
    xyz = ie_xyz_from_photons(spectral, display.wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    fig, ax = plt.subplots()
    ax.imshow(np.clip(srgb, 0.0, 1.0))
    ax.axis("off")
    ie_format_figure(ax)
    return ax
