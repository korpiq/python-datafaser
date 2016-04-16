import os
import sys


class FileLoader:

    def __init__(self, data, format_register, default_format=None):
        """
        :param data: datafaser.data.Data object to load into
        :param default_format: string name of format to use for files without a registered filename extension
        :param format_register: datafaser.formats.FormatRegister object providing file format modules
        """

        self.data = data
        self.default_format = default_format
        self.format_register = format_register

    def load(self, sources):
        """
        Loads data from files in given sources. Each source path must be relative and
        Each found file with a name ending in an extension mapped to a parser
        will be parsed with that parser. Contents will be added to
        data at path associated with the path of the file in source directory,
        so that contents of 'top/sub/key.txt' will be available at 'top.sub.key'.

        :param sources: list of strings: paths to files or directories to read
        """

        for source in sources:
            if source == '-':
                self._read_file(sys.stdin, self.default_format, None)
            elif isinstance(source, str):
                self._read_file_or_directory(_ensure_allowed_path(source))
            else:
                raise ValueError('File source name must be text: "%s" is %s' % (source, type(source)))

    def _read_file_or_directory(self, absolute_source):
        if os.path.isfile(absolute_source):
            _, extension = self._basename_and_extension(absolute_source)
            with open(absolute_source) as stream:
                self._read_file(stream, extension, None)
        elif os.path.isdir(absolute_source):
            self._read_directory(absolute_source)
        else:
            raise FileNotFoundError('Not a file or directory: "%s"' % absolute_source)

    def _read_directory(self, absolute_source):
        for path, dirs, filenames in os.walk(absolute_source):
            relative_path = path[len(absolute_source):]
            for filename in filenames:
                bare_name, extension = self._basename_and_extension(filename)
                key_path = relative_path.split(os.path.sep)[1:] + [bare_name]
                with open(os.path.join(path, filename)) as stream:
                    self._read_file(stream, extension, key_path)

    def _read_file(self, stream, extension, key_path):
        if self.format_register.is_known_filename_extension(extension):
            file_format = self.format_register.get_format_by_filename_extension(extension)
        elif self.format_register.is_known_format_name(self.default_format):
            file_format = self.format_register.get_format_by_name(self.default_format)
        else:
            raise FileExistsError(
                    'No content format associated with filename extension "%s": "%s"' % (extension, stream.name)
            )

        parsed = file_format.read(stream)
        if parsed is not None:
            self.data.merge(parsed, key_path=key_path)

    @staticmethod
    def _basename_and_extension(filename):
        parts = os.path.basename(filename).rsplit('.', 1)
        return parts[0], len(parts) > 1 and parts[1] or None


class FileSaver:

    def __init__(self, data, format_register):
        """
        :param data: raw data structure
        """

        self.data = data
        self.format_register = format_register

    def save(self, filename, output_format):
        """
        :param filename: string: path and name to file to write
        :param output_format: string: name of format to output
        """

        file_format = self.format_register.get_format_by_name(output_format)

        if filename == '-':
            file_format.write(self.data, sys.stdout)
        else:
            with open(_ensure_allowed_path(filename), 'w') as file:
                file_format.write(self.data, file)


def _ensure_allowed_path(filename):
    full_path = os.path.abspath(filename)
    current_dir = os.path.abspath(os.curdir)
    if full_path.startswith(current_dir):
        return full_path

    raise FileNotFoundError(
        'Will not access file "%s" outside current directory: "%s"' % (full_path, current_dir)
    )
