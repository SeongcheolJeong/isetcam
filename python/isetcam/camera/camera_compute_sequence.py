"""Compute a sequence of images using a camera model."""

from __future__ import annotations

from typing import Sequence, Tuple, List

import numpy as np

from .camera_class import Camera
from .camera_compute import camera_compute
from ..scene import Scene


def _ensure_sequence(val, n: int | None) -> tuple[list, bool]:
    """Return ``val`` as a list of length ``n`` and whether it was a sequence."""

    if isinstance(val, (list, tuple)):
        return list(val), True
    if n is None:
        return [val], False
    return [val for _ in range(n)], False


def camera_compute_sequence(
    camera: Camera,
    *,
    scenes: Sequence[Scene] | Scene,
    exposure_times: Sequence[float] | float = 1.0,
    n_frames: int | None = None,
) -> Tuple[Camera, List[np.ndarray]]:
    """Render ``camera`` for a sequence of scenes and exposure times.

    Parameters
    ----------
    camera:
        Camera object to update.
    scenes:
        One or more :class:`Scene` instances to render.
    exposure_times:
        Exposure time(s) corresponding to each frame.
    n_frames:
        Optional number of frames. When specified, a single ``scene`` or
        ``exposure_time`` will be replicated to match ``n_frames``.

    Returns
    -------
    camera : Camera
        Updated camera after processing the sequence.
    images : list of np.ndarray
        List of sensor ``volts`` arrays for each frame.
    """

    # Convert inputs to lists
    scenes_list, scenes_is_seq = _ensure_sequence(scenes, n_frames)
    exp_list, exp_is_seq = _ensure_sequence(exposure_times, n_frames)

    if n_frames is None:
        if scenes_is_seq and exp_is_seq and len(scenes_list) != len(exp_list):
            raise ValueError("Number of scenes must equal number of exposure_times")
        n_frames = max(len(scenes_list), len(exp_list))

    if len(scenes_list) not in {1, n_frames}:
        raise ValueError("Number of scenes must be 1 or n_frames")
    if len(exp_list) not in {1, n_frames}:
        raise ValueError("Number of exposure_times must be 1 or n_frames")

    if len(scenes_list) == 1:
        scenes_list *= n_frames
    if len(exp_list) == 1:
        exp_list *= n_frames

    images: List[np.ndarray] = []

    for sc, et in zip(scenes_list, exp_list):
        camera.sensor.exposure_time = float(et)
        camera = camera_compute(camera, sc)
        images.append(camera.sensor.volts.copy())

    return camera, images


__all__ = ["camera_compute_sequence"]
