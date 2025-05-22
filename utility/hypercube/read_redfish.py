import numpy as np
import h5py


def read_hdf5(path_file):
    """Load ReDFISh dataset from an HDF5 file.

    Parameters
    ----------
    path_file : str
        Path to the .h5 file containing the dataset.

    Returns
    -------
    hymg : np.ndarray
        Reflectance data cube normalised to [0, 1].
    color : np.ndarray
        RGB color image normalised to [0, 1].
    wave : np.ndarray
        Wavelength samples corresponding to the spectral planes.
    """
    with h5py.File(path_file, 'r') as f:
        keys = list(f.keys())
        # Load color image
        l_color_image = list(f[keys[0]])
        color = np.zeros((l_color_image[0].shape[1], l_color_image[0].shape[0], len(l_color_image)))
        color[:, :, 0] = l_color_image[0].T
        color[:, :, 1] = l_color_image[1].T
        color[:, :, 2] = l_color_image[2].T
        color = color / 255.0

        # Load reflectance cube
        l_reflectance = list(f[keys[1]])
        hymg = np.zeros((l_reflectance[0].shape[1], l_reflectance[0].shape[0], len(l_reflectance)))
        for w in range(len(l_reflectance)):
            hymg[:, :, w] = l_reflectance[w].T
        hymg = hymg / 65536.0

        # Load wavelength samples
        l_wavelength = list(f[keys[2]])
        wave = l_wavelength[0]

    return hymg, color, wave


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Read ReDFISh HDF5 file and print dataset shapes")
    parser.add_argument("path", help="Path to ReDFISh .h5 file")
    args = parser.parse_args()

    hymg, color, wave = read_hdf5(args.path)
    print("Reflectance cube shape:", hymg.shape)
    print("Color image shape:", color.shape)
    print("Wavelength shape:", wave.shape)
