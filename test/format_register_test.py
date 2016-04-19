import copy
import unittest
from datafaser.formats import FormatRegister, default_settings
import datafaser.formats.yaml


class FormatRegisterTest(unittest.TestCase):

    def setUp(self):
        self.register = FormatRegister(**copy.deepcopy(default_settings))

    def test_register_format_name(self):
        self._assert_error_from(
                'unknown format name',
                'Unknown format name: "sporaml"',
                self.register.get_format_by_name,
                'sporaml'
        )

        self.register.register('datafaser.formats.yaml', 'sporaml')

        self.assertIs(
                self.register.get_format_by_name('sporaml'),
                datafaser.formats.yaml,
                'FormatRegister returns correct module for a registered format name'
        )

    def test_register_format_with_extensions(self):
        self._assert_error_from(
                'unknown filename extension',
                'Unknown filename extension: "spora"',
                self.register.get_format_by_filename_extension,
                'spora'
        )

        self.register.register('datafaser.formats.yaml', 'sporaml', ['spora'])

        self.assertIs(
                self.register.get_format_by_filename_extension('spora'),
                datafaser.formats.yaml,
                'FormatRegister returns correct module for a registered filename extension'
        )

    def test_unregister_removes_format(self):
        self.assertIs(
            self.register.get_format_by_name('yaml'),
            datafaser.formats.yaml,
            'FormatRegister returns correct module for a known format name'
        )

        self.register.unregister('yaml')

        self._assert_error_from(
                'unregistered format name',
                'Unknown format name: "yaml"',
                self.register.get_format_by_name,
                'yaml'
        )

    def test_unregister_removes_filename_extension(self):
        self.assertIs(
                self.register.get_format_by_filename_extension('yml'),
                datafaser.formats.yaml,
                'FormatRegister returns correct module for a known filename extension'
        )

        self.register.unregister('yaml')

        self._assert_error_from(
                'unregistered file format extension',
                'Unknown filename extension: "yml"',
                self.register.get_format_by_filename_extension,
                'yml'
        )

    def _assert_error_from(self, case_name, error_message, method, *args):
        """
        :param case_name: string - title for the use case we assert
        :param error_message: string - expected exception message
        :param method: function - to call and expect an exception from
        :param args: list of arguments to function call
        :return: None
        """

        exception = self._return_exception_from(method, *args)

        message = 'FormatRegister.%s %%s on %s' % (method.__name__, case_name)
        self.assertIsInstance(exception, KeyError, message % 'fails')
        self.assertEquals("'%s'" % error_message, str(exception), message % 'reports error')

    def _return_exception_from(self, method, *args):
        try:
            method(*args)
        except Exception as e:
            return e
