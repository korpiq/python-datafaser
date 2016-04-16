import os
import unittest
from datafaser.files import FileLoader
from datafaser.data import Data
from test.files import path_to_test_data
from datafaser.formats import FormatRegister


class FileLoaderTest(unittest.TestCase):

    expected = {
        'yaml_files': {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}},
        'json_files': {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}},
        'text_files': {'a_text': 'foo is bar\n'}
    }

    def test_loads_nothing_ok(self):
        data = {}
        loader = FileLoader(Data(data))
        loader.load([])
        self.assertEquals({}, data, 'Loader loads nothing')

    def test_loads_yaml_map_ok(self):
        data = Data({})
        loader = FileLoader(data)
        loader.load(path_to_test_data('yaml_files', 'a_map.yaml'))
        self.assertEquals(self.expected['yaml_files']['a_map'], data.data, 'Loader loads contents from yaml file')

    def test_loads_yaml_ok(self):
        data = {}
        loader = FileLoader(Data(data))
        loader.load(path_to_test_data('yaml_files'))
        self.assertEquals(self.expected['yaml_files'], data, 'Loader loads yaml')

    def test_loads_json_ok(self):
        data = {}
        loader = FileLoader(Data(data))
        loader.load(path_to_test_data('json_files'))
        self.assertEquals(self.expected['json_files'], data, 'Loader loads json')

    def test_loads_text_ok(self):
        data = {}
        loader = FileLoader(Data(data))
        loader.load(path_to_test_data('text_files'))
        self.assertEquals(self.expected['text_files'], data, 'Loader loads text')

    def test_loading_without_parser_fails(self):
        data = {}
        loader = FileLoader(Data(data))
        exception = None
        try:
            loader.load(path_to_test_data('ignored_files'))
        except Exception as e:
            exception = e
        self.assertIsNotNone(exception, 'Loading with unknown extension must fail')

    def test_loads_mixed_formats_skipping_extensionless_ok(self):
        register = FormatRegister()
        register.register('datafaser.formats.ignore', None)
        data = {}
        loader = FileLoader(Data(data), format_register=register)
        loader.load(path_to_test_data())
        self.assertEquals(self.expected, data, 'Loader loads all supported types of data')

    def test_loads_mixed_formats_with_default_parser_ok(self):
        data = {}
        loader = FileLoader(Data(data), default_format='text')
        loader.load(path_to_test_data())
        expected = self.expected.copy()
        expected['ignored_files'] = {'filename_without_extension': 'This file name no extension, such wild.\n'}
        self.assertEquals(expected, data, 'Loader loads all supported types of data')

    def test_load_with_absolute_path_fails(self):
        loader = FileLoader(Data({}))
        exception = None
        try:
            loader.load(['/test/loader/testdata/text_files'])
        except Exception as e:
            exception = e

        self.assertIsNotNone(exception, 'Loading from absolute path must fail')

    def test_load_with_backtracking_path_fails(self):
        loader = FileLoader(Data({}))
        exception = None
        try:
            loader.load(os.path.sep.join(['..', path_to_test_data()]))
        except Exception as e:
            exception = e

        self.assertIsNotNone(exception, 'Loading from backtracking path must fail')
