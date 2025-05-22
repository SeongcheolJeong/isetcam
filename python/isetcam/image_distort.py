import numpy as np
from PIL import Image
from .utils import ie_clip


def image_distort(img: np.ndarray, method: str = 'gaussian noise', *args) -> np.ndarray:
    """Apply simple image distortion methods.

    Parameters
    ----------
    img : np.ndarray
        Input image array.
    method : str, optional
        Distortion method. Supported methods are ``'gaussian noise'`` and
        ``'scale contrast'``.
    args : tuple
        Additional arguments specific to the method.

    Returns
    -------
    np.ndarray
        Distorted image array.
    """
    method = method.lower().replace(' ', '')

    if method == 'gaussiannoise':
        n_scale = args[0] if args else 0.05 * float(img.max())
        noise = n_scale * np.random.randn(*img.shape)
        result = img.astype(float) + noise
        if np.issubdtype(img.dtype, np.integer) and img.max() < 256:
            result = ie_clip(result, 0, 255).astype(img.dtype)
        return result

    if method == 'scalecontrast':
        s = args[0] if args else 0.1
        return img * (1 + s)

    raise ValueError(f'Unknown method: {method}')
