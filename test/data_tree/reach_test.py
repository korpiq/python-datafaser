import unittest
import datafaser.data_tree


class DataTreeAccessTest(unittest.TestCase):

    def setUp(self):
        self.data_tree = datafaser.data_tree.DataTree({'foo': [{'bar': 'baz'}, {'quu': 'faz'}]})

    def test_dig_deep_ok(self):
        self.assertEqual('faz', self.data_tree.reach('foo.1.quu'), 'Access nested dictionary and list elements')

    def test_dig_deep_missing(self):
        self.assertEqual('\'Missing "bar" in "foo.1"\'', self._miss('foo.1.bar'), 'Expect error for missing element')

    def test_dig_invalid_list_index(self):
        self.assertEqual(
                '\'Invalid list index "bar" at "foo": ValueError invalid literal for int() with base 10: \\\'bar\\\'\'',
                self._miss('foo.bar'),
                'Expect error for invalid list key'
        )

    def test_dig_stops_at_scalar(self):
        self.assertEqual(
                '\'No container at "foo.0.bar" trying to get "foo.0.bar.0"\'',
                self._miss('foo.0.bar.0'),
                'Expect error for attempting access into scalar'
        )

    def _miss(self, *args, **kwargs):
        try:
            self.data_tree.reach(*args, **kwargs)
        except KeyError as e:
            return str(e)
