"""Scene-related functions."""

from .scene_class import Scene
from .scene_add import scene_add
from .scene_utils import get_photons, set_photons, get_n_wave
from .scene_from_file import scene_from_file
from .scene_from_ddf_file import scene_from_ddf_file
from .scene_from_basis import scene_from_basis
from .scene_get import scene_get
from .scene_set import scene_set
from .scene_adjust_luminance import scene_adjust_luminance
from .scene_adjust_illuminant import scene_adjust_illuminant
from .scene_adjust_reflectance import scene_adjust_reflectance
from .scene_calculate_luminance import scene_calculate_luminance
from .scene_create import scene_create
from .scene_photon_noise import scene_photon_noise
from .scene_crop import scene_crop
from .scene_pad import scene_pad
from .scene_insert import scene_insert
from .scene_translate import scene_translate
from .scene_rotate import scene_rotate
from .scene_spd_scale import scene_spd_scale
from .scene_spatial_support import scene_spatial_support
from .scene_spatial_resample import scene_spatial_resample
from .scene_frequency_support import scene_frequency_support
from .scene_frequency_resample import scene_frequency_resample
from .scene_interpolate_w import scene_interpolate_w
from .scene_to_file import scene_to_file
from .scene_extract_waveband import scene_extract_waveband
from .scene_add_grid import scene_add_grid
from .scene_grid_lines import scene_grid_lines
from .scene_checkerboard import scene_checkerboard
from .scene_combine import scene_combine
from .scene_adjust_pixel_size import scene_adjust_pixel_size
from .scene_show_image import scene_show_image
from .scene_save_image import scene_save_image
from .scene_thumbnail import scene_thumbnail
from .scene_illuminant_pattern import scene_illuminant_pattern
from .scene_illuminant_ss import scene_illuminant_ss
from .scene_illuminant_scale import scene_illuminant_scale
from .scene_hdr_image import scene_hdr_image
from .scene_hdr_chart import scene_hdr_chart
from .scene_hdr_lights import scene_hdr_lights
from .scene_create_hdr import scene_create_hdr
from .scene_depth_overlay import scene_depth_overlay
from .scene_depth_range import scene_depth_range
from .scene_list import scene_list
from .scene_make_video import scene_make_video
from .scene_dead_leaves import scene_dead_leaves
from .scene_wb_create import scene_wb_create
from .scene_plot import scene_plot
from .scene_description import scene_description
from .scene_clear_data import scene_clear_data
from .scene_init_geometry import scene_init_geometry
from .scene_init_spatial import scene_init_spatial
from .scene_vector_utils import (
    scene_photons_from_vector,
    scene_energy_from_vector,
)
from .scene_radiance_from_vector import scene_radiance_from_vector

__all__ = [
    "Scene",
    "scene_add",
    "get_photons",
    "set_photons",
    "get_n_wave",
    "scene_from_file",
    "scene_from_ddf_file",
    "scene_from_basis",
    "scene_get",
    "scene_set",
    "scene_adjust_luminance",
    "scene_adjust_illuminant",
    "scene_adjust_reflectance",
    "scene_calculate_luminance",
    "scene_crop",
    "scene_pad",
    "scene_insert",
    "scene_translate",
    "scene_rotate",
    "scene_spd_scale",
    "scene_spatial_support",
    "scene_spatial_resample",
    "scene_frequency_support",
    "scene_frequency_resample",
    "scene_interpolate_w",
    "scene_create",
    "scene_photon_noise",
    "scene_to_file",
    "scene_extract_waveband",
    "scene_add_grid",
    "scene_grid_lines",
    "scene_checkerboard",
    "scene_combine",
    "scene_adjust_pixel_size",
    "scene_show_image",
    "scene_plot",
    "scene_save_image",
    "scene_thumbnail",
    "scene_illuminant_pattern",
    "scene_illuminant_ss",
    "scene_illuminant_scale",
    "scene_depth_overlay",
    "scene_depth_range",
    "scene_list",
    "scene_dead_leaves",
    "scene_wb_create",
    "scene_description",
    "scene_clear_data",
    "scene_hdr_image",
    "scene_hdr_chart",
    "scene_hdr_lights",
    "scene_create_hdr",
    "scene_make_video",
    "scene_init_geometry",
    "scene_init_spatial",
    "scene_photons_from_vector",
    "scene_energy_from_vector",
    "scene_radiance_from_vector",
]
