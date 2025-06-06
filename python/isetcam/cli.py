# mypy: ignore-errors
"""Command line interface for ISETCam utilities."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import runpy

import isetcam




def _cmd_info(args: argparse.Namespace) -> int:
    """Print package version and repository root."""
    print(f"isetcam {isetcam.__version__}")
    print(isetcam.iset_root_path())
    return 0


def _cmd_list_scenes(args: argparse.Namespace) -> int:
    """List sample scene names."""
    from isetcam.scene import scene_list

    for name in scene_list():
        print(name)
    return 0


def _cmd_run_tests(args: argparse.Namespace) -> int:
    """Run the Python unit tests using pytest."""
    root = isetcam.iset_root_path()
    cmd = [sys.executable, "-m", "pytest", "-q"]
    result = subprocess.run(cmd, cwd=root)
    return result.returncode


def _cmd_pipeline(args: argparse.Namespace) -> int:
    """Run a simple camera pipeline and save the result."""
    from isetcam.scene import scene_create
    from isetcam.camera import camera_create, camera_compute, camera_to_file
    from isetcam.opticalimage import oi_compute
    from isetcam.sensor import sensor_compute

    cam = camera_create()
    cam.name = f"Camera-{args.scene}"
    scene = scene_create(args.scene)
    oi = oi_compute(scene, cam.optics)
    cam.optical_image = oi
    cam.sensor = sensor_compute(cam.sensor, oi)
    camera_compute(cam, cam.sensor)
    camera_to_file(cam, args.output)
    return 0


def _available_tutorials() -> list[str]:
    """Return a sorted list of available tutorial script names."""
    base = Path(__file__).resolve().parents[1] / "tutorials"
    names: list[str] = []
    for path in base.rglob("*.py"):
        if path.name.startswith("t_"):
            rel = path.relative_to(base).with_suffix("")
            names.append(str(rel))
    names.sort()
    return names


def _cmd_tutorial(args: argparse.Namespace) -> int:
    """Run a tutorial script under ``python/tutorials``."""
    base = Path(__file__).resolve().parents[1] / "tutorials"
    script = base / f"{args.name}.py"
    if not script.is_file():
        print(f"Tutorial not found: {args.name}", file=sys.stderr)
        return 1
    runpy.run_path(script, run_name="__main__")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``isetcam`` command."""
    parser = argparse.ArgumentParser(prog="isetcam")
    subparsers = parser.add_subparsers(dest="command")

    p_info = subparsers.add_parser("info", help="Show version information")
    p_info.set_defaults(func=_cmd_info)

    p_list = subparsers.add_parser("list-scenes", help="List available scenes")
    p_list.set_defaults(func=_cmd_list_scenes)

    p_tests = subparsers.add_parser("run-tests", help="Run the unit tests")
    p_tests.set_defaults(func=_cmd_run_tests)

    p_pipe = subparsers.add_parser("pipeline", help="Run a demo pipeline")
    p_pipe.add_argument("--scene", required=True, help="Scene name")
    p_pipe.add_argument("--output", required=True, help="Output MAT-file path")
    p_pipe.set_defaults(func=_cmd_pipeline)

    tut_list = ', '.join(_available_tutorials())
    p_tut = subparsers.add_parser(
        "tutorial",
        help="Run a tutorial script",
        description="Run a tutorial script. Available: " + tut_list,
    )
    p_tut.add_argument("name", help="Tutorial script name")
    p_tut.set_defaults(func=_cmd_tutorial)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover - script entry
    sys.exit(main())
