from datafaser.data_tree import DataTree
from datafaser.files import FileLoader, FileSaver
from datafaser.formats import FormatRegister


def get_default_operations_map(data):
    return {
        'load': Loader(data).load
    }


class Loader:
    def __init__(self, data_tree):
        self.format_register = FormatRegister(**data_tree.dig('datafaser.formats'))

    def load(self, data_tree, directives):
        new_data = DataTree({})

        if 'from' in directives:
            for source in directives['from']:
                if 'files' in source:
                    if not isinstance(source, dict):
                        raise TypeError('Not a dict: %s: "%s"' % (type(source), source))
                    FileLoader(new_data, self.format_register).load(source['files'])
                if 'data' in source:
                    for key in source['data']:
                        new_data.merge(data_tree.dig(key))

        if 'to' in directives:
            self.save(data_tree, new_data, directives['to'])
        else:
            data_tree.merge(new_data.data)

    def save(self, data_tree, new_data, targets):
        for target in targets:
            if 'data' in target:
                data_tree.merge(new_data.data, target['data'])
            if 'files' in target:
                writer = FileSaver(new_data.data, self.format_register)
                for output_format, filename in target['files'].items():
                    writer.save(filename, output_format)
