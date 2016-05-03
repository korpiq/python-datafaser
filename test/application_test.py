import sys
import unittest
from subprocess import Popen, PIPE


class ApplicationTest(unittest.TestCase):

    def test_start_ok(self):
        stdout, stderr, status = self._call()
        self.assertEquals(stdout, b'', 'datafaser without arguments produces no standard output')
        self.assertNotRegexpMatches(stderr, b'ERROR', 'datafaser without arguments produces no error messages')
        self.assertEquals(status, 0, 'datafaser without arguments exits ok')

    def test_help_ok(self):
        stdout, stderr, status = self._call('--help')
        self.assertEquals(stdout, b'', 'Option --help produces no standard output')
        self.assertRegexpMatches(stderr, b'--help', 'Option --help explains usage')
        self.assertEqual(status, 1, 'Option --help exits with status 1')

    def test_unrecognized_option_fails(self):
        stdout, stderr, status = self._call('--unrecognized-option')
        self.assertEquals(stdout, b'', 'Unrecognized option produces no standard output')
        self.assertRegexpMatches(stderr, b'--help', 'Unrecognized option explains usage')
        self.assertEquals(status, 2, 'Unrecognized option exits with status 2')

    def _call(self, *options):
        full_command = [sys.executable, 'datafaser'] + list(options)
        process = Popen(full_command, stderr=PIPE, stdout=PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode
