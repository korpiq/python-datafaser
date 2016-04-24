import os
from copy import deepcopy
import unittest
import tempfile

from datafaser.data_tree import DataTree
from datafaser.run import Runner
from datafaser import formats
from test.files import path_to_test_data


class RunnerTest(unittest.TestCase):

    _read_yaml_plan = [{'load': {'from': [{'files': path_to_test_data('yaml_files')}]}}]
    _read_yaml_result = {'a_list': ['foo', 'bar'], 'a_map': {'foo': 'bar'}}
    _minimum_required_settings = {
        'datafaser': {
            'formats': formats.default_settings
        }
    }

    _read_schema_plan = [{'load': {'from': [{'files': path_to_test_data('test_data_schema.json')}]}}]

    _runnable_configuration = deepcopy(_minimum_required_settings)
    _runnable_configuration['datafaser']['run'] = {
        'plan': [{'test_phase': _read_yaml_plan + _read_schema_plan}]
    }

    def setUp(self):
        self.data_tree = DataTree(deepcopy(self._minimum_required_settings))
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
        Runner(self.data_tree).run_operation(deepcopy(self._read_yaml_plan))
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

    def test_running_unknown_operation_fails(self):
        runner = Runner(self.data_tree)
        exception = self._get_exception_from(runner.run_operation, [{'xyzzy': []}])
        self.assertIsInstance(exception, ValueError, 'Invalid operation raises ValueError')
        self.assertEqual(
                'Unknown operation: "xyzzy"',
                str(exception),
                'Invalid operation raises expected error message'
        )

    def test_run_plan_ok(self):
        expected = deepcopy(self._runnable_configuration['datafaser']['run']['plan'])
        runner = Runner(DataTree(deepcopy(self._runnable_configuration)))

        runner.load_and_run_all_plans()

        self.assertEquals('bar', runner.data_tree.reach('a_map.foo'), 'Run loads data')
        self.assertEquals([], runner.data_tree.reach('datafaser.run.plan'), 'Run empties plan')
        self.assertEquals(expected, runner.data_tree.reach('datafaser.run.done'), 'Run empties plan')

    def test_run_empty_phase_fails(self):
        plan = deepcopy(self._runnable_configuration)
        plan['datafaser']['run']['plan'] = [{}]
        runner = Runner(DataTree(plan))

        exception = self._get_exception_from(runner.load_and_run_all_plans)

        self.assertIsInstance(exception, ValueError, 'Empty phase raises ValueError')
        self.assertEqual(
                'Phase #1 in plan does not map one name to operations: {}',
                str(exception),
                'Empty phase raises expected error message'
        )

    def test_run_phase_with_multiple_names_fails(self):
        plan = deepcopy(self._runnable_configuration)
        plan['datafaser']['run']['plan'] = [{'A': [], 'B': []}]
        runner = Runner(DataTree(plan))

        exception = self._get_exception_from(runner.load_and_run_all_plans)

        self.assertIsInstance(exception, ValueError, 'Phase with multiple names raises ValueError')
        self.assertRegexpMatches(
                str(exception),
                "^Phase #1 in plan does not map one name to operations\\b",
                'Phase with multiple names raises expected error message'
        )

    def test_validation_failure(self):
        plan = deepcopy(self._runnable_configuration)
        plan['schema'] = {
            'additionalProperties': False
        }
        plan['XYZZY'] = 'not allowed by schema'
        runner = Runner(DataTree(plan))

        exception = self._get_exception_from(runner.load_and_run_all_plans)

        self.assertIsInstance(exception, ValueError, 'Data not matching schema raises ValueError')
        self.assertEqual(
                '1 errors after phase #1',
                str(exception),
                'Data not matching schema raises expected error message'
        )

    def _get_exception_from(self, method, *args):
        try:
            return method(*args)
        except Exception as e:
            return e
