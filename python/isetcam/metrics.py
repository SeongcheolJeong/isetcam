import math
from typing import Sequence


def exposure_value(f_number: float, exposure_time: float) -> float:
    """Calculate the exposure value (EV).

    Parameters
    ----------
    f_number : float
        The f-number of the optics.
    exposure_time : float
        Exposure duration in seconds.

    Returns
    -------
    float
        The exposure value computed as ``log2((f_number ** 2) / exposure_time)``.
    """
    if exposure_time <= 0:
        raise ValueError("exposure_time must be positive")
    if f_number <= 0:
        raise ValueError("f_number must be positive")
    return math.log2((f_number ** 2) / exposure_time)


def _sum_squared_error(im1: Sequence, im2: Sequence) -> tuple[float, int]:
    """Return sum of squared error and element count for two arrays."""
    if len(im1) != len(im2):
        raise ValueError("Input images must have the same dimensions")
    err = 0.0
    count = 0
    for a, b in zip(im1, im2):
        if isinstance(a, Sequence) and not isinstance(a, (bytes, bytearray)):
            sub_err, sub_count = _sum_squared_error(a, b)
            err += sub_err
            count += sub_count
        else:
            diff = float(a) - float(b)
            err += diff * diff
            count += 1
    return err, count


def _mean_square_error(im1: Sequence, im2: Sequence) -> float:
    err, count = _sum_squared_error(im1, im2)
    return err / count if count else 0.0


def iepsnr(im1: Sequence, im2: Sequence) -> float:
    """Compute Peak Signal-to-Noise Ratio (PSNR) between two images.

    Parameters
    ----------
    im1, im2 : sequence of numbers or nested sequences
        Input images with the same shape. Pixel values are assumed to be in
        the range [0, 255].

    Returns
    -------
    float
        The PSNR value in decibels. Returns ``math.inf`` when the images are
        identical.
    """
    mse = _mean_square_error(im1, im2)
    if mse == 0:
        return math.inf
    return 20 * math.log10(255.0 / math.sqrt(mse))
