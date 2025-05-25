import numpy as np
from typing import Iterable, Union

def ie_clip(im: np.ndarray, lower_bound: Union[float, None] = 0, upper_bound: Union[float, None] = 1) -> np.ndarray:
    """Clip image data to a specified range.

    Parameters
    ----------
    im : np.ndarray
        Input array to be clipped.
    lower_bound : float or None, optional
        Lower bound of the clip. ``None`` means no lower clipping.
    upper_bound : float or None, optional
        Upper bound of the clip. ``None`` means no upper clipping.

    Returns
    -------
    np.ndarray
        The clipped array. The returned array has the same dtype as the input.
    """
    result = im.astype(float)
    if lower_bound is not None:
        result[result < lower_bound] = lower_bound
    if upper_bound is not None:
        result[result > upper_bound] = upper_bound
    return result.astype(im.dtype)


def ie_param_format(value: Union[str, Iterable]) -> Union[str, Iterable]:
    """Convert strings to ISET parameter format (lower case, no spaces).

    If ``value`` is an iterable, only the items at even indices are converted.

    Parameters
    ----------
    value : str or iterable
        String or a list of key/value pairs.

    Returns
    -------
    str or iterable
        Formatted string or iterable with formatted keys.
    """
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        return value.lower().replace(' ', '')

    if isinstance(value, Iterable):
        result = list(value)
        for i in range(0, len(result), 2):
            if isinstance(result[i], str):
                result[i] = ie_param_format(result[i])
        return type(value)(result)

    return value
