"""Replace an existing object in ``vcSESSION``."""

from __future__ import annotations

from typing import Any

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_replace_object(obj_type: str, obj: Any, index: int | None = None) -> int:
    """Replace an object stored in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Type of the object to replace.
    obj : Any
        Object instance that will overwrite the stored entry.
    index : int, optional
        Index to replace. Defaults to the currently selected object of
        ``obj_type`` or ``1`` if none is selected.

    Returns
    -------
    int
        The index of the replaced object.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field, 1)
    if index is None or index < 1:
        index = 1

    lst = vcSESSION.setdefault(field, [None])
    while len(lst) <= index:
        lst.append(None)
    lst[index] = obj
    vcSESSION[field] = lst

    vcSESSION.setdefault("SELECTED", {})[field] = index
    return index
