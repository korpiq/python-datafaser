import copy
import unittest

from datafaser.data_tree import DataTree
from datafaser.operations.load import Loader
from test import minimum_required_settings


class LoadTest(unittest.TestCase):

    def setUp(self):
        self.loader = Loader(DataTree(copy.deepcopy(minimum_required_settings)))

    def test_load_without_directives_ok(self):
        target = {}
        self.loader.load(DataTree(target), {})
        self.assertEquals({}, target, 'Empty result for empy directives')

    def test_load_nothing_to_data_ok(self):
        target = {'There': 'Misty Mountain'}
        back = target.copy()
        self.loader.load(DataTree(target), {'to': {'branch': 'Back'}})
        self.assertEquals({'There': 'Misty Mountain', 'Back': back}, target,
                          'Loading nothing to nonexistent key copies whole data to target')

    def test_load_from_data_to_data_ok(self):
        target = {'There': 'Misty Mountain'}
        self.loader.load(DataTree(target), {'from': {'branch': 'There'}, 'to': {'branch': 'Back'}})
        self.assertEquals({'There': 'Misty Mountain', 'Back': 'Misty Mountain'}, target,
                          'Loading from data to data copies the source to the target')

    def test_load_from_list_fails(self):
        exception = self._exception_from_loading_with({}, {'from': []})
        self.assertIsInstance(exception, TypeError, 'Invalid from structure causes type error')

    def _exception_from_loading_with(self, source, directives):
        try:
            self.loader.load(DataTree(source), directives)
        except Exception as e:
            return e
