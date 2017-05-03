import unittest

from datafaser.data_tree import DataTree
from datafaser.operations import table


class TableConversionTest(unittest.TestCase):

    def test_objects_from_single_header(self):
        list_of_lists = {
            'list_of_lists': [
                ['head1', 'head2'],
                ['val1-1', 'val1-2'],
                ['val2-1', 'val2-2']
            ]
        }
        expected = [
            {'head1': 'val1-1', 'head2': 'val1-2'},
            {'head1': 'val2-1', 'head2': 'val2-2'}
        ]
        data_tree = DataTree(list_of_lists)
        directives = {
            'from': {
                'table': {
                    'branch': 'list_of_lists',
                    'headers': [{'rows': 1}]
                }
            },
            'to': {'branch': 'actual'}
        }
        table.convert(data_tree, directives)
        self.assertEqual(data_tree.reach('actual'), expected)
