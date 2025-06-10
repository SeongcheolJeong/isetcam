# mypy: ignore-errors
"""Basic optical image plotting utilities."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore
    Rectangle = None  # type: ignore

from .oi_class import OpticalImage
from ..ie_param_format import ie_param_format
from ..opticalimage.oi_calculate_illuminance import oi_calculate_illuminance
from ..opticalimage.oi_calculate_irradiance import oi_calculate_irradiance
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb
from ..display import Display, display_render, display_apply_gamma
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format
from ..ie_format_figure import ie_format_figure


_DEF_KINDS = {
    "illuminancehline",
    "illuminancevline",
    "irradiancehline",
    "irradiancevline",
    "irradianceimage",
    "irradianceimagewithgrid",
}


def _photons_to_srgb(oi: OpticalImage, display: Display) -> np.ndarray:
    photons = np.asarray(oi.photons, dtype=float)
    spd = np.asarray(display.spd, dtype=float)
    xw, rows, cols = rgb_to_xw_format(photons)
    # Convert the spectral data to display RGB values. ``spd`` has shape
    # ``(n_wave, 3)``, hence we use the pseudoinverse of its transpose.
    rgb_lin = xw @ np.linalg.pinv(spd.T)
    if display.gamma is not None:
        rgb = display_apply_gamma(rgb_lin, display, inverse=True)
    else:
        rgb = rgb_lin
    rgb = xw_to_rgb_format(rgb, rows, cols)
    spectral = display_render(rgb, display, apply_gamma=True)
    xyz = ie_xyz_from_photons(spectral, display.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    return np.clip(srgb, 0.0, 1.0)


def oi_plot(
    oi: OpticalImage,
    kind: str = "illuminancehline",
    loc: int | None = None,
    *,
    grid_spacing: int | None = None,
    roi: tuple[int, int, int, int] | None = None,
    display: Display | None = None,
    ax: "plt.Axes | None" = None,
) -> "plt.Axes":
    """Plot properties of ``oi`` similar to MATLAB ``oiPlot``."""
    if plt is None:
        raise ImportError("matplotlib is required for oi_plot")

    key = ie_param_format(kind)
    if key not in _DEF_KINDS:
        raise ValueError(f"Unknown plot kind '{kind}'")

    rows, cols = oi.photons.shape[:2]

    if key in {"illuminancehline", "illuminancevline"}:
        illum = oi_calculate_illuminance(oi)
        if key == "illuminancehline":
            r = rows // 2 if loc is None else int(loc)
            profile = illum[r, :]
            pos = np.arange(cols)
            xlabel = "Column index"
        else:
            c = cols // 2 if loc is None else int(loc)
            profile = illum[:, c]
            pos = np.arange(rows)
            xlabel = "Row index"
        if ax is None:
            _, ax = plt.subplots()
        ax.plot(pos, profile, "r-")
        ie_format_figure(ax, xlabel=xlabel, ylabel="Illuminance (lux)")
        return ax

    if key in {"irradiancehline", "irradiancevline"}:
        irr = oi_calculate_irradiance(oi)
        if key == "irradiancehline":
            r = rows // 2 if loc is None else int(loc)
            profile = irr[r, :]
            pos = np.arange(cols)
            xlabel = "Column index"
        else:
            c = cols // 2 if loc is None else int(loc)
            profile = irr[:, c]
            pos = np.arange(rows)
            xlabel = "Row index"
        if ax is None:
            _, ax = plt.subplots()
        ax.plot(pos, profile, "r-")
        ie_format_figure(ax, xlabel=xlabel, ylabel="Irradiance (photons)")
        return ax

    if display is None:
        # Simple identity display matching the optical image wavelengths
        display = Display(spd=np.eye(len(oi.wave)), wave=oi.wave, gamma=None)
    img = _photons_to_srgb(oi, display)
    if ax is None:
        _, ax = plt.subplots()
    ax.imshow(img)
    ax.axis("off")

    if grid_spacing is not None:
        g = int(grid_spacing)
        for r in range(0, rows, g):
            ax.axhline(r - 0.5, color="k", linewidth=0.5)
        for c in range(0, cols, g):
            ax.axvline(c - 0.5, color="k", linewidth=0.5)
    if roi is not None and Rectangle is not None:
        r0, c0, h, w = [int(v) for v in roi]
        rect = Rectangle((c0, r0), w, h, edgecolor="y", facecolor="none", linewidth=1)
        ax.add_patch(rect)

    ie_format_figure(ax)
    return ax


__all__ = ["oi_plot"]
