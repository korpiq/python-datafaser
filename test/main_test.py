import os
import sys
import unittest
import runpy
import datafaser


class MainTest(unittest.TestCase):

    def setUp(self):
        self.original_argv = sys.argv
        self.original_path = sys.path
        self.original_run = datafaser.run

    def tearDown(self):
        sys.argv = self.original_argv
        sys.path = self.original_path
        datafaser.run = self.original_run

    def test_starts_ok(self):
        self.got_files = None
        self._run_main()
        self.assertEqual(sys.argv[1:], self.got_files, 'main calls run with command-line arguments without program name')

    def test_fixes_path_ok(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path = list(filter(lambda part: part != base_dir, sys.path))
        self._run_main()
        self.assertIn(base_dir, sys.path, 'main adds datafaser to path')

    def _run_main(self):
        datafaser.run = self._mock_start
        sys.argv = ['some', 'strings']
        runpy.run_module('datafaser', run_name='__main__')

    def _mock_start(self, files):
        self.got_files = files
