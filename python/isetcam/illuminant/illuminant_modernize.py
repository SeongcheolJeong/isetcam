"""Convert legacy illuminant structures to :class:`Illuminant`."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .illuminant_class import Illuminant


def illuminant_modernize(illuminant: Any) -> Illuminant:
    """Return ``illuminant`` as an :class:`Illuminant` instance."""

    if isinstance(illuminant, Illuminant):
        return illuminant

    if not isinstance(illuminant, Mapping):
        raise TypeError("Illuminant must be mapping or Illuminant")

    # Wavelength information
    if "wave" in illuminant:
        wave = np.asarray(illuminant["wave"], dtype=float).reshape(-1)
    elif "wavelength" in illuminant:
        wave = np.asarray(illuminant["wavelength"], dtype=float).reshape(-1)
    elif isinstance(illuminant.get("spectrum"), Mapping) and "wave" in illuminant["spectrum"]:
        wave = np.asarray(illuminant["spectrum"]["wave"], dtype=float).reshape(-1)
    else:
        raise ValueError("Illuminant missing wavelength data")

    # Spectral data
    data = illuminant.get("data")
    spd = None
    if isinstance(data, Mapping):
        if "photons" in data:
            spd = np.asarray(data["photons"], dtype=float).reshape(-1)
        elif "energy" in data:
            spd = np.asarray(data["energy"], dtype=float).reshape(-1)
    elif data is not None:
        spd = np.asarray(data, dtype=float).reshape(-1)

    if spd is None and "photons" in illuminant:
        spd = np.asarray(illuminant["photons"], dtype=float).reshape(-1)

    if spd is None:
        raise ValueError("Illuminant missing spectral data")

    name = illuminant.get("name")
    if name is not None:
        name = str(name)

    return Illuminant(spd=spd, wave=wave, name=name)


__all__ = ["illuminant_modernize"]
