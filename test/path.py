import unittest
from datafaser.path import DataPath


class DataPathConstructionTest(unittest.TestCase):

    def test_construction_ok_on_empty_list(self):
        DataPath([])

    def test_construction_with_wrong_parameter_type_fails(self):
        self.assertRaises(ValueError, DataPath, {})

    def test_construction_with_varying_list_content_types_ok(self):
        DataPath(["a string", 123, {}, []])


class DataPathFindFromListTest(unittest.TestCase):

    data_structure = ["first item", "middle item", "last item"]

    def test_find_one_returns_a_list_item_as_requested_ok(self):
        self.assertEqual(
            DataPath([1]).find_one_from(self.data_structure),
            [([1], self.data_structure[1])]
        )

    def test_find_past_list_end_returns_empty_ok(self):
        self.assertEqual(
            DataPath([9]).find_each_from(self.data_structure),
            []
        )

    def test_find_one_past_list_end_fails(self):
        self.assertRaises(KeyError, DataPath([9]).find_one_from, self.data_structure)


class DataPathFindFromDeepStructureTest(unittest.TestCase):

    data_structure = {
        "a string": "this is a string",
        "a list": [
            "first list item",
            "middle list item",
            "last list item"
        ],
        "a dictionary": {
            "first item": "this is the first item",
            "second item": "this is an item",
            "middle item": "this is the middle item",
            "second to last item": "this is an item",
            "last item": "this is the last item"
        }
    }

    def test_find_one_returns_whole_structure_for_empty_path_ok(self):
        self.assertEqual(
            DataPath([]).find_each_from(self.data_structure),
            [([], self.data_structure)]
        )

    def test_find_returns_items_for_first_level_scalar_path_elements_ok(self):
        for key, value in self.data_structure.items():
            self.assertEqual(
                DataPath([key]).find_each_from(self.data_structure),
                [([key], value)]
            )

    def test_find_returns_items_for_second_level_scalar_path_elements_ok(self):
        for path in [["a list", 1], ["a dictionary", "first item"]]:
            self.assertEqual(
                DataPath(path).find_each_from(self.data_structure),
                [(path, self.data_structure[path[0]][path[1]])]
            )

    def test_find_returns_empty_for_missing_element_ok(self):
        self.assertEqual(
            DataPath(["missing key"]).find_each_from({}),
            []
        )

    def test_find_one_from_missing_element_fails(self):
        self.assertRaises(KeyError, DataPath(["missing key"]).find_one_from, {})

    def test_find_returns_all_equal_values_ok(self):
        needle = "this is an item"
        self.assertEqual(
            DataPath(["a dictionary", {"value": needle}]).find_each_from(self.data_structure),
            [
                (["a dictionary", "second item"], needle),
                (["a dictionary", "second to last item"], needle)
            ]
        )
