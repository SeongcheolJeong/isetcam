"""Generate a pure tone similar to the MATLAB ``ieTone`` function."""

from __future__ import annotations

import numpy as np

try:
    import sounddevice as sd
    _HAS_SOUNDDEVICE = True
except Exception:  # sounddevice may not be installed
    _HAS_SOUNDDEVICE = False


def ie_tone(
    frequency: float = 256.0,
    amplitude: float = 0.2,
    duration: float = 0.25,
    fs: float = 8192.0,
    play: bool = False,
) -> np.ndarray:
    """Create (and optionally play) a tone.

    Parameters
    ----------
    frequency : float
        Tone frequency in Hertz.
    amplitude : float
        Amplitude of the tone.
    duration : float
        Duration of the tone in seconds.
    fs : float
        Sampling frequency in Hertz.
    play : bool
        If ``True`` and ``sounddevice`` is available, play the tone.

    Returns
    -------
    numpy.ndarray
        Array containing the tone samples.
    """
    t = np.arange(0, fs * duration + 1) / fs
    y = amplitude * np.sin(2 * np.pi * frequency * t)
    if play and _HAS_SOUNDDEVICE:
        sd.play(y, samplerate=int(fs))
        sd.wait()
    return y
