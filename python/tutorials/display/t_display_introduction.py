import numpy as np
import matplotlib.pyplot as plt
from isetcam import ie_init, data_path
from isetcam.display import display_create, display_plot
from isetcam.scene import scene_from_file, scene_adjust_illuminant, Scene, scene_show_image
from isetcam.illuminant import illuminant_create


def main():
    ie_init()

    # Create a display and visualize some of its characteristics
    disp = display_create("OLED-Samsung")
    display_plot(disp, kind="spd")
    display_plot(disp, kind="gamma")
    display_plot(disp, kind="gamut")

    # Load an image and convert it to a scene using the display model
    img_path = data_path("images/rgb/eagle.jpg")
    scene = scene_from_file(img_path)
    scene_show_image(scene)

    # Change the illuminant while preserving reflectance
    fl_path = data_path("lights/Fluorescent.mat")
    scene2 = scene_adjust_illuminant(scene, fl_path)
    scene2.name = "fluorescent"
    scene_show_image(scene2)

    # Adjust illuminant using a D50 light
    ill = illuminant_create("d50", scene.wave)
    scene3 = scene_adjust_illuminant(scene, ill.spd)
    scene3.name = "d50"
    scene_show_image(scene3)

    return scene.photons.shape, scene2.photons.shape, scene3.photons.shape


if __name__ == "__main__":
    main()
