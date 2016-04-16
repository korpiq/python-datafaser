import io
import sys
import unittest
from datafaser.files import FileSaver
from datafaser.formats import FormatRegister, default_settings


class FileWriterStdoutTest(unittest.TestCase):

    def setUp(self):
        self._stdout = sys.stdout
        self.buffer = io.StringIO()
        sys.stdout = self.buffer

    def tearDown(self):
        sys.stdout = self._stdout

    def test_write_yaml_to_stdout_ok(self):
        FileSaver({'foo': ['bar']}, FormatRegister(**default_settings)).save('-', 'yaml')
        expected = 'foo:\n- bar\n'
        self.assertEqual(expected, self.buffer.getvalue(), 'Yaml written in expected format to STDOUT')

    def test_write_json_to_stdout_ok(self):
        FileSaver({'foo': ['bar']}, FormatRegister(**default_settings)).save('-', 'json')
        expected = '{\n    "foo": [\n        "bar"\n    ]\n}\n'
        self.assertEqual(expected, self.buffer.getvalue(), 'Json written in expected format to STDOUT')

    def test_write_text_to_stdout_ok(self):
        expected = 'Hello there!'
        FileSaver(expected, FormatRegister(**default_settings)).save('-', 'text')
        self.assertEqual(expected, self.buffer.getvalue(), 'Text written in expected format to STDOUT')

    def test_write_dict_as_text_to_stdout_fails(self):
        exception = None
        try:
            FileSaver({}, FormatRegister(**default_settings)).save('-', 'text')
        except Exception as e:
            exception = e
        self.assertIsNotNone(exception, 'Dictionary not written as text')
