import sys
import unittest
import subprocess


class ApplicationTest(unittest.TestCase):

    def test_start_ok(self):
        subprocess.check_call([sys.executable, 'datafaser'])
