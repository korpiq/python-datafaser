import logging

from datafaser.data_tree import DataTree
from datafaser.files import FileLoader, FileSaver
from datafaser.formats import FormatRegister


class Loader:
    """
    Copy data structures between different sources and targets such as files and memory.
    """

    def __init__(self, data_tree):
        """
        :param data_tree: DataTree object holding datafaser.formats configuration for FormatRegister
        """

        self.format_register = FormatRegister(**data_tree.reach('datafaser.formats'))
        self.data_tree = data_tree
        self.logger = logging.getLogger(__name__)

    def load(self, data_tree, directives):

        if 'from' in directives:
            new_data = DataTree({})
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
                        FileLoader(new_data, self.format_register, self._get_default_format()).load(source_values)
                    elif source_type == 'data':
                        for key in source_values:
                            new_data.merge(data_tree.reach(key))
                    else:
                        raise KeyError('Unknown load source type: "%s"' % source_type)
        else:
            new_data = DataTree(data_tree.data.copy())

        if 'to' in directives:
            self._save_new_data(data_tree, new_data, directives['to'])
        else:
            data_tree.merge(new_data.data)

    def _save_new_data(self, data_tree, new_data, target):
        if not isinstance(target, dict):
            raise TypeError('Not a dictionary of target types to targets to save to: %s' % type(target).__name__)

        if 'data' in target:
            self.logger.info('Store read data at: "%s"' % target['data'])
            data_tree.merge(new_data.data, target['data'])

        if 'file' in target:
            self.logger.info('Save read data to: "%s"' % target['file'])

            writer = FileSaver(new_data.data, self.format_register)
            filename = target['file']
            if not isinstance(filename, str):
                raise TypeError('Not a filename to save to: %s' % type(filename).__name__)

            output_format = target.get('format') or self._get_default_format()
            if not isinstance(output_format, str):
                raise ValueError('Missing format for file to write: "%s"' % filename)
            writer.save(filename, output_format)

    def _get_default_format(self):
        return self.data_tree.reach('datafaser.run').get('options', {}).get('default-format')
