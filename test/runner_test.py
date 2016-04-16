import os
import unittest

from datafaser.data import Data
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
        self.data = Data(self._minimum_required_settings.copy())
        self.runner = Runner(self.data)
        self.maxDiff = None

    def test_construct_ok(self):
        pass

    def test_run_empty_ok(self):
        Runner(self.data).run_operation([])
        del self.data.data['datafaser']
        self.assertEquals({}, self.data.data, 'Empty run does not add data')

    def test_run_load_nothing_ok(self):
        Runner(self.data).run_operation([{'load': {}}])
        self.assertEquals(self._minimum_required_settings, self.data.data, 'Empty load list does not add data')

    def test_run_load_zero_files_ok(self):
        Runner(self.data).run_operation([{'load': {'from': [{'files': []}]}}])
        self.assertEquals(self._minimum_required_settings, self.data.data, 'Empty load files list does not add data')

    def test_run_load_yaml_from_directory_ok(self):
        Runner(self.data).run_operation(self._read_yaml_plan.copy())
        del self.data.data['datafaser']
        self.assertEquals(self._read_yaml_result, self.data.data, 'Load files from directory adds data')

    def test_run_load_to_data_ok(self):
        plan = [{'load': {'from': self._read_yaml_plan[0]['load']['from'], 'to': [{'data': 'inner.target'}]}}]
        Runner(self.data).run_operation(plan)
        expected = {'inner': {'target': self._read_yaml_result}}
        expected.update(self._minimum_required_settings)
        self.assertEquals(expected, self.data.data, 'Load files from directory adds to specified place in data')
