import unittest

from datafaser.data_tree import DataTree
from datafaser.operations.fill import convert


class FillTest(unittest.TestCase):

    def test_fill_ok(self):
        data_tree = DataTree({
            'source': {'A': 1},
            'template': 'Here be {{ A }}.'
        })
        expected = 'Here be 1.'
        directives = {
            'from': { 'branch': 'source' },
            'to': { 'branch': 'target' },
            'template': 'template'
        }
        convert(data_tree, directives)
        self.assertEquals(data_tree.reach('target'), expected, 'Template has been filled out.')
