"""Create a :class:`Scene` from a basis representation."""

from __future__ import annotations

from typing import Mapping, Any

import numpy as np

from .scene_class import Scene
from ..illuminant import illuminant_modernize


_DEF_IMG_MEAN = None  # placeholder for mypy-type hints


def _reshape_coeffs(mc: np.ndarray) -> tuple[np.ndarray, tuple[int, int] | None]:
    """Return coefficient matrix in XW format and original spatial size."""
    mc = np.asarray(mc, dtype=float)
    if mc.ndim == 3:
        h, w, n = mc.shape
        return mc.reshape(h * w, n), (h, w)
    if mc.ndim == 2:
        return mc, None
    raise ValueError("mcCOEF must be 2-D or 3-D")


def _reshape_photons(flat: np.ndarray, shape: tuple[int, int] | None, n_wave: int) -> np.ndarray:
    if shape is None:
        return flat
    h, w = shape
    return flat.reshape(h, w, n_wave)


def scene_from_basis(sceneS: Mapping[str, Any]) -> Scene:
    """Return a :class:`Scene` reconstructed from ``sceneS``."""

    if "mcCOEF" not in sceneS:
        raise KeyError("mcCOEF required")
    if "basis" not in sceneS:
        raise KeyError("basis required")

    basis_struct = sceneS["basis"]
    if not isinstance(basis_struct, Mapping) or "basis" not in basis_struct or "wave" not in basis_struct:
        raise KeyError("basis must contain 'basis' and 'wave'")

    coeffs, shape = _reshape_coeffs(sceneS["mcCOEF"])
    basis = np.asarray(basis_struct["basis"], dtype=float)
    wave = np.asarray(basis_struct["wave"], dtype=float).reshape(-1)

    photons_flat = coeffs @ basis.T
    photons = _reshape_photons(photons_flat, shape, wave.size)

    if "imgMean" in sceneS and sceneS["imgMean"] is not None:
        mean = np.asarray(sceneS["imgMean"], dtype=float).reshape(-1)
        if photons.ndim == 3:
            photons = photons + mean.reshape(1, 1, -1)
        else:
            photons = photons + mean

    photons = np.maximum(photons, 0.0)

    scene = Scene(photons=photons, wave=wave)

    illum = sceneS.get("illuminant")
    if illum is not None:
        scene.illuminant = illuminant_modernize(illum)

    return scene


__all__ = ["scene_from_basis"]
