# Python Support for ISETCam

This directory contains experimental Python code that mirrors portions of the
MATLAB ISETCam toolbox.  To use these modules, activate the Python environment
that accompanies the MATLAB examples. Installing the package will pull in
`numpy`, `scipy`, `pillow`, `imageio`, and `scikit-image` automatically.

```bash
# Create the environment
conda create -n py39 python=3.9

# Activate it
conda activate py39

# Install the dependencies
pip install -r requirements.txt

# Install the package in editable mode (installs the requirements as well)
pip install -e .
```

Inside MATLAB, point `pyenv` to the environment's Python interpreter:

```matlab
pyenv('Version','/opt/miniconda3/envs/py39/bin/python');
```

For a detailed walkthrough see `s_python.m` in this folder.

The ``isetcam`` package includes lightweight dataclasses for ``Scene``,
``OpticalImage`` and ``Sensor`` objects along with helper functions.  To
validate the installation run the unit tests:

```bash
export PYTHONPATH=$PWD/python
pytest -q
```

These tests are also executed automatically via
[GitHub Actions](../.github/workflows/python-tests.yml).
