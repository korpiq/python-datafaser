import unittest

from datafaser.start import *
from test.files import path_to_test_data


class RunnerTest(unittest.TestCase):

    files_key = 'datafaser.run.%s.0.test loading files.%d.load.from.file'
    files = [
        path_to_test_data('json_files'),
        path_to_test_data('text_files'),
        path_to_test_data('test_data_schema.json')
    ]

    def test_construction_ok(self):
        data_tree = DataTree(create_datafaser_structure_to_load_files(self.files, 'test loading files'))
        actual = [data_tree.reach(self.files_key % ('plan', i)) for i in range(0,len(self.files))]
        self.assertEquals(
                actual,
                self.files,
                'Start plans to load filenames given to constructor'
        )

    def test_run_plan_ok(self):
        runner = create_runner_to_load(self.files, 'test loading files')
        runner.load_and_run_all_plans()

        self.assertEquals('bar', runner.data_tree.reach('a_map.foo'), 'Run loads data')
        self.assertEquals([], runner.data_tree.reach('datafaser.run.plan'), 'Run empties plan')
        self.assertEquals(self.files[-1], runner.data_tree.reach(self.files_key % ('done', len(self.files)-1)), 'Run done load')
