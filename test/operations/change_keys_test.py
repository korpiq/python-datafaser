import unittest

from datafaser.data_tree import DataTree
from datafaser.operations.change import map_keys


class KeyMappingTest(unittest.TestCase):

    a_dict = {
        'A': 1,
        'B': 2,
        'C': 3
    }

    mapping = {
        'A': 'AA',
        'B': 'BB'
    }

    def setUp(self):
        self.data_tree = DataTree({'source': self.a_dict})

    def test_mapping_keys_keep_ok(self):
        expected = {
            'AA': 1,
            'BB': 2,
            'C': 3
        }
        map_keys(self.data_tree, self._directives('keep'))
        self.assertEqual(self.data_tree.reach('actual'), expected)

    def test_mapping_keys_deny_ok(self):
        with self.assertRaisesRegex(KeyError, 'Unmatched keys: "C"'):
            map_keys(self.data_tree, self._directives('deny'))

    def _directives(self, others):
        return {
            'from': {'branch': 'source'},
            'to': {'branch': 'actual'},
            'keys': self.mapping,
            'others': others
        }
