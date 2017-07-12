

class DataPath:

    def __init__(self, list_of_path_elements):
        if isinstance(list_of_path_elements, list):
            self.list_of_path_elements = list_of_path_elements
        else:
            raise ValueError("Data path created without a list of path elements")

    def find_one_from(self, data_structure):
        selection = self.find_each_from(data_structure)
        if len(selection) != 1:
            if len(selection) < 1:
                raise KeyError("No value found at path: %s" % self)
            else:
                raise KeyError("Multiple values found at path: %s" % self)
        return selection

    def find_each_from(self, data_structure):
        selection = [([], data_structure)]

        for path_element in self.list_of_path_elements:
            if isinstance(path_element, dict):
                selection = _select(selection, _selector_for_value, path_element)
            else:
                selection = _select(selection, _selector_for_key, path_element)

        return selection

    def __str__(self):
        return str(self.list_of_path_elements)


def _select(candidates, selector, *args):
    selection = []

    for candidate in candidates:
        selection.extend(selector(*candidate, *args))

    return selection


def _selector_for_key(path, collection, select_key):
    selection = []

    if _collection_contains_key(collection, select_key):
        selection.append((path + [select_key], collection[select_key]))

    return selection


def _collection_contains_key(collection, key):
    if isinstance(collection, dict):
        return key in collection
    elif isinstance(collection, list):
        return 0 <= key < len(collection)
    return False


def _selector_for_value(path, collection, criteria):
    return _select_by_value([(path, collection)], criteria['value'])


def _select_by_value(candidates, select_value):
    selection = []

    for candidate in candidates:
        path, collection = candidate
        for key, value in collection.items():
            if select_value == value:
                selection.append((path + [key], value))

    return selection
