from datafaser.data_tree import DataTree
from datafaser.files import FileLoader, FileSaver
from datafaser.formats import FormatRegister


def get_default_operations_map(data):
    return {
        'load': Loader(data).load
    }


class Loader:
    """
    Copy data structures between different sources and targets such as files and memory.
    """

    def __init__(self, data_tree):
        """
        :param data_tree: DataTree object holding datafaser.formats configuration for FormatRegister
        """

        self.format_register = FormatRegister(**data_tree.reach('datafaser.formats'))

    def load(self, data_tree, directives):
        new_data = DataTree({})

        if 'from' in directives:
            sources = directives['from']
            if not isinstance(sources, list):
                raise TypeError('Not a list of sources to load from: %s' % type(sources).__name__)
            for source in sources:
                if not isinstance(source, dict):
                    raise TypeError('Not a dictionary of sources to load from: %s' % type(source).__name__)
                for source_type, source_values in source.items():
                    if not isinstance(source_values, list):
                        raise TypeError(
                                'Not a list of %s sources to load from: %s' %
                                (source_type, type(source_values).__name__)
                        )
                    if source_type == 'files':
                        FileLoader(new_data, self.format_register).load(source['files'])
                    elif source_type == 'data':
                        for key in source['data']:
                            new_data.merge(data_tree.reach(key))
                    else:
                        raise KeyError('Unknown load source type: "%s"' % source_type)

        if 'to' in directives:
            self.save(data_tree, new_data, directives['to'])
        else:
            data_tree.merge(new_data.data)

    def save(self, data_tree, new_data, targets):
        if not isinstance(targets, list):
            raise TypeError('Not a list of targets to save to: %s' % type(targets).__name__)
        for target in targets:
            if not isinstance(target, dict):
                raise TypeError('Not a dictionary of target types to targets to save to: %s' % type(target).__name__)
            if 'data' in target:
                data_tree.merge(new_data.data, target['data'])
            if 'files' in target:
                writer = FileSaver(new_data.data, self.format_register)
                for output_format, filename in target['files'].items():
                    if not isinstance(output_format, str):
                        raise TypeError('Not a name of an output format: %s' % type(output_format).__name__)
                    if not isinstance(filename, str):
                        raise TypeError('Not a filename to save to: %s' % type(filename).__name__)
                    writer.save(filename, output_format)
