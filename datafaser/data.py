"""
Operations on plain deep data structures.
"""

class Data:

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
