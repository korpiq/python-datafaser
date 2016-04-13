import os
import sys


class FileLoader:

    class Parsers:

        @staticmethod
        def yaml(stream):
            import yaml
            return yaml.load(stream)

        @staticmethod
        def json(stream):
            import json
            return json.load(stream)

        @staticmethod
        def text(stream):
            return stream.read()

        @staticmethod
        def ignore(stream):
            pass

    parsers = {
        'yaml': Parsers.yaml,
        'yml': Parsers.yaml,
        'json': Parsers.json,
        'text': Parsers.text,
        'txt': Parsers.text,
        'skip': Parsers.ignore
    }

    def __init__(self, data, default_format=None, parsers=None):
        """
        :param data: datafaser.data.Data object to load into
        :param parsers: map of file extensions to parser functions
        """
        self.data = data
        self.default_format = default_format
        if parsers:
            self.parsers = parsers

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
            else:
                self._read_file_or_directory(_ensure_allowed_path(source))

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
        if extension in self.parsers:
            parser = self.parsers[extension]
        elif self.default_format in self.parsers:
            parser = self.parsers[self.default_format]
        else:
            raise FileExistsError('File format unknown: "%s"' % stream.name)

        parsed = parser(stream)
        if parsed is not None:
            self.data.merge(parsed, key_path=key_path)

    @staticmethod
    def _basename_and_extension(filename):
        parts = os.path.basename(filename).rsplit('.', 1)
        return parts[0], len(parts) > 1 and parts[1] or None


def _ensure_allowed_path(filename):
    full_path = os.path.abspath(filename)
    current_dir = os.path.abspath(os.curdir)
    if full_path.startswith(current_dir):
        return full_path

    raise FileNotFoundError(
        'Will not access file "%s" outside current directory: "%s"' % (full_path, current_dir)
    )
