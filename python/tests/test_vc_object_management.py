import numpy as np

from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_get_object,
    vc_replace_object,
    vc_replace_and_select_object,
)
from isetcam.scene import Scene
from isetcam.ie_init_session import vcSESSION


def test_vc_get_object():
    ie_init()
    s1 = Scene(photons=np.zeros((1, 1, 1)))
    s2 = Scene(photons=np.ones((1, 1, 1)))
    idx1 = vc_add_and_select_object("scene", s1)
    idx2 = vc_add_and_select_object("scene", s2)

    assert vc_get_object("scene", idx1) is s1
    assert vc_get_object("scene") is s2
    assert vcSESSION["SELECTED"]["SCENE"] == idx2


def test_vc_replace_object():
    ie_init()
    s1 = Scene(photons=np.zeros((1, 1, 1)))
    vc_add_and_select_object("scene", s1)

    s2 = Scene(photons=np.ones((1, 1, 1)))
    idx = vc_replace_object("scene", s2)

    assert idx == 1
    assert vcSESSION["SCENE"][1] is s2
    assert vcSESSION["SELECTED"]["SCENE"] == 1


def test_vc_replace_and_select_object():
    ie_init()
    s1 = Scene(photons=np.zeros((1, 1, 1)))
    idx = vc_add_and_select_object("scene", s1)

    s2 = Scene(photons=np.ones((1, 1, 1)))
    out_idx = vc_replace_and_select_object("scene", s2, idx)

    assert out_idx == idx
    assert vcSESSION["SCENE"][idx] is s2
    assert vcSESSION["SELECTED"]["SCENE"] == idx
