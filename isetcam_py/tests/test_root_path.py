import unittest
from pathlib import Path
import sys
import os

# Add the repository root to sys.path so isetcam_py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from isetcam_py import root_path


class TestRootPath(unittest.TestCase):
    def test_root_path_exists(self):
        rp = root_path()
        self.assertIsInstance(rp, Path)
        self.assertTrue((rp / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
