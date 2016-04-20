import os
import unittest
import tempfile

from datafaser.data_tree import DataTree
from datafaser.run import Runner
from datafaser import formats


class RunnerTest(unittest.TestCase):

    _read_yaml_plan = [{'load': {'from': [{'files': [os.path.join('test', 'test_data', 'yaml_files')]}]}}]
    _read_yaml_result = {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}}
    _minimum_required_settings = {
        'datafaser': {
            'formats': formats.default_settings
        }
    }

    def setUp(self):
        self.data_tree = DataTree(self._minimum_required_settings.copy())
        self.runner = Runner(self.data_tree)
        self.maxDiff = None

    def test_construct_ok(self):
        pass

    def test_run_empty_ok(self):
        Runner(self.data_tree).run_operation([])
        del self.data_tree.data['datafaser']
        self.assertEquals({}, self.data_tree.data, 'Empty run does not add data')

    def test_run_load_nothing_ok(self):
        Runner(self.data_tree).run_operation([{'load': {}}])
        self.assertEquals(self._minimum_required_settings, self.data_tree.data, 'Empty load list does not add data')

    def test_run_load_zero_files_ok(self):
        Runner(self.data_tree).run_operation([{'load': {'from': [{'files': []}]}}])
        self.assertEquals(self._minimum_required_settings, self.data_tree.data, 'Empty load files list does not add data')

    def test_run_load_yaml_from_directory_ok(self):
        Runner(self.data_tree).run_operation(self._read_yaml_plan.copy())
        del self.data_tree.data['datafaser']
        self.assertEquals(self._read_yaml_result, self.data_tree.data, 'Load files from directory adds data')

    def test_run_load_to_data_ok(self):
        plan = [{'load': {'from': self._read_yaml_plan[0]['load']['from'], 'to': [{'data': 'inner.target'}]}}]
        Runner(self.data_tree).run_operation(plan)
        expected = {'inner': {'target': self._read_yaml_result}}
        expected.update(self._minimum_required_settings)
        self.assertEquals(expected, self.data_tree.data, 'Load files from directory adds to specified place in data')

    def test_run_load_data_to_files_ok(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with tempfile.TemporaryDirectory(dir=os.path.join(base_dir, 'local')) as temp_dir:
            temp_file = os.path.join(temp_dir, 'file_writing_test.output')
            plan = [{'load': {'from': [{'data': ['test.data']}], 'to': [{'files': {'json': temp_file}}]}}]
            self.data_tree.data.update({'test': {'data': {'key': 'test value'}}})
            Runner(self.data_tree).run_operation(plan)
            expected = '{\n    "key": "test value"\n}\n'
            with open(temp_file) as file:
                self.assertEqual(expected, file.read(), 'Json written in expected format to file')
