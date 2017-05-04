import unittest

from datafaser.data_tree import DataTree
from datafaser.operations.each import convert


class EachOperationTest(unittest.TestCase):

    def test_each_change_ok(self):
        data_tree = DataTree({
            'source': [{'old': 1}, {'old': 2}],
            'datafaser': {'formats': {
                'format_handlers_by_name': {},
                'formats_by_filename_extension': {}
            }}
        })
        expected = [{'new': 1}, {'new': 2}]
        directives = {
            'from': { 'branch': 'source' },
            'to': { 'branch': 'target' },
            'do': {
                'change': {
                    'keys': {'old': 'new'},
                    'others': 'deny'
                }
            }
        }
        convert(data_tree, directives)
        self.assertEquals(data_tree.reach('target'), expected, 'Operation has been applied for each object')
