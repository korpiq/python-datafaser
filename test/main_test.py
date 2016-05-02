import os
import sys
import unittest
import runpy
from datafaser import operations


class MainTest(unittest.TestCase):

    _schema_path_required_for_validation = 'schema.properties.datafaser.properties.run.properties.options.properties'

    def setUp(self):
        self.original_argv = sys.argv
        self.original_path = sys.path
        self.original_operations_provider = operations.get_default_operations_map

    def tearDown(self):
        sys.argv = self.original_argv
        sys.path = self.original_path
        operations.get_default_operations_map = self.original_operations_provider

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
        operations.get_default_operations_map = self._mock_operations_map
        sys.argv = ['some', 'strings']
        runpy.run_module('datafaser', run_name='__main__')

    def _mock_operations_map(self, _):
        return {'load': self._mock_load}

    def _mock_load(self, data_tree, directives):
        self.got_files = directives['from'][0]['files']
        self._create_schema_required_for_validation(data_tree)

    def _create_schema_required_for_validation(self, data_tree):
        data_tree.reach(self._schema_path_required_for_validation, create_containers=True)
