# Python Utilities for ISETCam

This folder contains Python modules that replicate small portions of
ISETCam functionality.  The goal is to gradually migrate useful MATLAB
functions to Python.

Currently implemented:

- `ie_read_spectra`: load spectral data stored in MATLAB `.mat` files
  and interpolate to arbitrary wavelength samples.

## Running the tests

Tests are written using Python's built-in `unittest` module.  Run them
from the repository root with:

```bash
PYTHONPATH=python python -m unittest discover python/tests
```
