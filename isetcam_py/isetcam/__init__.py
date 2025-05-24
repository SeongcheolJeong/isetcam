from pathlib import Path


def root_path() -> Path:
    """Return the absolute path to the ISETCam repository root."""
    return Path(__file__).resolve().parents[2]


__all__ = ["root_path"]
