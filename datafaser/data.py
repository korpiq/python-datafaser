"""
Operations on plain deep data structures.
"""

class Data:
    """
    Data object contains a free form data structure.

    Nested dictionaries and lists can be accessed with key lists.

    Dictionary contents can be merged and lists appended to.

    Other data types can only be stored as leaves of the data tree structure.
    """

    def __init__(self, data, separator='.'):
        self.data = data is None and {} or data
        self.separator = separator

    def dig(self, key_path, create_containers=False):
        if isinstance(key_path, str):
            key_path = key_path.split(self.separator)
        data = self.data

        for index, key in enumerate(key_path):
            if isinstance(data, dict):
                if key not in data:
                    if create_containers:
                        data[key] = {}
                    else:
                        raise KeyError('Missing "%s" in "%s"' % (key, self.separator.join(key_path[:index])))
                data = data[key]
            elif isinstance(data, list):
                try:
                    data = data[int(key)]
                except Exception as e:
                    raise KeyError('Invalid list index "%s" at "%s": %s %s' %
                        (key, self.separator.join(key_path[:index]), e.__class__.__name__, str(e)))
            else:
                raise KeyError('No container at "%s" trying to get "%s"' %
                    (self.separator.join(key_path[:index]), self.separator.join(key_path)))

        return data                

    def merge(self, add_data, key_path=None):
        if key_path and len(key_path):
           my_data = self.dig(key_path, create_containers=True)
        else:
           my_data = self.data
           key_path = []

        result = self._merge_node(add_data, my_data, [], {})

        if len(key_path):
            self.dig(key_path[:-1])[key_path[-1]] = result
        else:
            self.data = result

    def _merge_node(self, add_data, my_data, key_path, results):
        if isinstance(add_data, dict):
            if isinstance(my_data, dict):
                return self._merge_dictionaries(add_data, my_data, key_path, results)
        elif isinstance(add_data, list):
            if isinstance(my_data, list):
                return my_data + add_data

        return add_data

    def _merge_dictionaries(self, add_data, my_data, key_path, results):

        my_id = id(my_data)
        if my_id in results:  # cyclic reference already being merged.
            return results[my_id]

        new_data = my_data.copy()
        results[my_id] = new_data

        for key, value in add_data.items():
            if key in my_data:
                new_data[key] = self._merge_node(value, my_data[key], key_path + [key], results)
            else:
                new_data[key] = value
        
        return new_data

