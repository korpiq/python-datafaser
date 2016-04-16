__all__ = ['ignore', 'json', 'text', 'yaml']


class FormatRegister:
    """
    FormatRegister provides extensible reference point for file formats.
    You can provide a custom FormatRegister for access to files in exceptional formats.
    Default is to provide datafaser.formats.*

    Each format is only imported when actually used, so that applications that do not use
    formats such as yaml do not need to depend on unnecessary external libraries.

    Each format module provides functions to read and write streams in that format.
    """

    default_filename_extension_mapping = {
        'yml': 'yaml',
        'txt': 'text',
        'skip': 'ignore'
    }

    def __init__(self, format_module_names_by_name=None, formats_by_file_extension=None):
        if format_module_names_by_name:
            self.format_module_names_by_name = format_module_names_by_name
        else:
            self.format_module_names_by_name = {key: __name__ + '.' + key for key in __all__}

        if formats_by_file_extension:
            self.formats_by_file_extension = formats_by_file_extension
        else:
            self.formats_by_file_extension = {}
            for key in self.format_module_names_by_name.keys():
                self.formats_by_file_extension[key] = key
            self.formats_by_file_extension.update(self.default_filename_extension_mapping)

    def get_format_by_name(self, name):
        full_name = self.format_module_names_by_name[name]
        namespace, relative_name = full_name.rsplit('.', 1)
        return __import__(full_name, fromlist=[relative_name])

    def get_format_by_filename_extension(self, extension):
        return self.get_format_by_name(self.formats_by_file_extension[extension])

    def is_known_filename_extension(self, extension):
        if extension in self.formats_by_file_extension:
            return True

    def register(self, module_name, format_name, filename_extension_list=None):
        self.format_module_names_by_name[format_name] = module_name
        if filename_extension_list:
            for extension in filename_extension_list:
                self.formats_by_file_extension[extension] = format_name

    def unregister(self, format_name):
        del self.format_module_names_by_name[format_name]
        for key, value in self.formats_by_file_extension.items():
            if value == format_name:
                del self.formats_by_file_extension[key]
