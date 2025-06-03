import numpy as np
import matplotlib.pyplot as plt
from isetcam import ie_init, data_path, ie_read_spectra
from isetcam.display import display_create, display_apply_gamma


def main():
    ie_init()

    disp = display_create("OLED-Samsung")
    # Use only RGB primaries
    disp.spd = disp.spd[:, :3]
    disp.gamma = disp.gamma[:, :3]
    wave = disp.wave

    # Load reflectance data and illuminant
    refl, _, _, _ = ie_read_spectra(data_path("surfaces/reflectances/macbethChart.mat"), wave)
    d65, _, _, _ = ie_read_spectra(data_path("lights/D65.mat"), wave)
    xyz_cmfs, _, _, _ = ie_read_spectra(data_path("human/XYZ.mat"), wave)

    d65 = d65.reshape(-1)
    macbeth_xyz = xyz_cmfs.T @ (d65[:, None] * refl)

    phosphors = disp.spd
    rgb_lin = np.linalg.inv(xyz_cmfs.T @ phosphors) @ macbeth_xyz
    rgb_lin /= rgb_lin.max()

    # Scale so that the white patch is [1,1,1]
    wht = rgb_lin[:, 3]
    rgb_lin = (1 / wht)[:, None] * rgb_lin

    digital = display_apply_gamma(rgb_lin.T, disp, inverse=True)
    digital /= digital.max()

    patch = digital.reshape(4, 6, 3).transpose(1, 0, 2)
    img = np.kron(patch, np.ones((20, 20, 1)))

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis("off")

    return patch


if __name__ == "__main__":
    main()
