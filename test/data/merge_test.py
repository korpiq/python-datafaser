import unittest
from datafaser.data import Data

class DataTest(unittest.TestCase):

     def test_merge_scalar_ok(self):
         result = self._merge('foo', 'bar')
         self.assertEqual('bar', result, 'Overwrites scalar even on top level')

     def test_merge_toplevel_list_appends_ok(self):
         l1 = ['foo']
         l2 = ['bar']
         result = self._merge(l1, l2)
         self.assertIsNot(l1, result, 'Original list not used')
         self.assertIsNot(l2, result, 'Added list not used')
         self.assertEqual(['foo','bar'], result, 'New list contains new items after old ones')

     def test_merge_inner_list_appends_ok(self):
         l1 = {'a': {'b': ['foo']}}
         l2 = {'a': {'b': ['bar']}}
         result = self._merge(l1, l2)
         self.assertIsNot(l1, result, 'Original list not used')
         self.assertIsNot(l2, result, 'Added list not used')
         self.assertEqual({'a': {'b': ['foo','bar']}}, result, 'New list contains new items after old ones')

     def test_merge_dict_adds_key_ok(self):
         d1 = {'foo': 1}
         d2 = {'bar': 2}
         result = self._merge(d1, d2)
         self.assertIsNot(d1, result, 'Original dict not used')
         self.assertIsNot(d2, result, 'Added dict not used')
         self.assertEqual({'foo': 1, 'bar': 2}, result, 'New dict contains both old and new items')

     def test_merge_scalar_overwrites_ok(self):
         d1 = {'foo': {'bar': 1}, 'baz': 2}
         d2 = {'foo': 'quu'}
         result = self._merge(d1, d2)
         self.assertIsNot(d1, result, 'Original dict not used')
         self.assertIsNot(d2, result, 'Added dict not used')
         self.assertEqual({'foo': 'quu', 'baz': 2}, result, 'New dict contains overriding item')

     def test_merge_self_containing_structures_ok(self):
         d1 = {'foo': {'zer': 'zor'}, 'zup': 'zop'}
         d1['foo']['bar'] = d1
         d2 = {'foo': {'baz': 'quu'}, 'zip': 'zap'}
         d2['foo']['bar'] = d2
         expected = {'foo': {'baz': 'quu', 'zer': 'zor'}, 'zip': 'zap', 'zup': 'zop'}
         expected['foo']['bar'] = expected
         result = self._merge(d1, d2)
         self.assertEqual(expected, result, 'Dicts are merged with back reference')

     def _merge(self, data1, data2):
         d = Data(data1)
         d.merge(data2)
         return d.data
