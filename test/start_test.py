import unittest

from datafaser.start import Start
from test.files import path_to_test_data


class RunnerTest(unittest.TestCase):

    files_key = 'datafaser.run.%s.0.start.0.load.from.0.files'

    def test_construction_ok(self):
        args = []
        start = Start(args)
        self.assertIs(args, start.data.dig(self.files_key % 'plan'),
                      'Start plans to load filenames given to constructor')

    def test_run_plan_ok(self):
        args = path_to_test_data('json_files') + path_to_test_data('text_files')
        start = Start(args)
        start.load_and_run_all_plans()
        self.assertEquals('bar', start.data.dig('a_map.foo'), 'Run loads data')
        self.assertEquals([], start.data.dig('datafaser.run.plan'), 'Run empties plan')
        self.assertEquals(args, start.data.dig(self.files_key % 'done'), 'Run done load')
