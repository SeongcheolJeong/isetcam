"""Replace an object in ``vcSESSION`` and set it as selected."""

from __future__ import annotations

from typing import Any

from .ie_init_session import vcSESSION
from .vc_replace_object import vc_replace_object
from .vc_add_and_select_object import _norm_objtype


def vc_replace_and_select_object(
    obj_type: str, obj: Any, index: int | None = None
) -> int:
    """Replace an object and select it."""
    field = _norm_objtype(obj_type)
    idx = vc_replace_object(obj_type, obj, index)
    vcSESSION.setdefault("SELECTED", {})[field] = idx
    return idx
