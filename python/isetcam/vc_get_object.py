"""Retrieve an object from ``vcSESSION``."""

from __future__ import annotations

from typing import Any

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_get_object(obj_type: str, index: int | None = None) -> Any:
    """Return an object stored in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Object type name.
    index : int, optional
        Index of the desired object. When omitted the currently selected
        object of ``obj_type`` is returned.

    Returns
    -------
    Any
        The requested object or ``None`` if not found.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)

    lst = vcSESSION.get(field)
    if index is None or lst is None or index <= 0 or index >= len(lst):
        return None

    return lst[index]
