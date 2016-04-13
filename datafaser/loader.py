import os


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
        'json': Parsers.json,
        'txt': Parsers.text,
        'skip': Parsers.ignore
    }

    def __init__(self, data, parsers=None):
        """
        :param data: datafaser.data.Data object to load into
        :param parsers: map of file extensions to parser functions
        """
        self.data = data
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
            absolute_source = os.path.abspath(source)
            current_dir = os.path.abspath(os.curdir)
            if not absolute_source.startswith(current_dir):
                raise FileNotFoundError('Path must be inside current directory "%s": "%s"' % (current_dir, source))

            if os.path.isfile(absolute_source):
                _, extension = self._basename_and_extension(absolute_source)
                self._read_file(absolute_source, extension, None)
            elif os.path.isdir(absolute_source):
                for path, dirs, filenames in os.walk(absolute_source):
                    relative_path = path[len(absolute_source):]
                    for filename in filenames:
                        bare_name, extension = self._basename_and_extension(filename)
                        key_path = relative_path.split(os.path.sep)[1:] + [bare_name]
                        self._read_file(os.path.join(path, filename), extension, key_path)
            else:
                raise FileNotFoundError('Not a file or directory: "%s"' % source)

    def _read_file(self, filepath, extension, key_path):
        if extension in self.parsers:
            with open(filepath) as stream:
                parsed = self.parsers[extension](stream)
                if parsed is not None:
                    self.data.merge(parsed, key_path=key_path)
        else:
            raise FileExistsError('Unsupported file: "%s"' % filepath)

    @staticmethod
    def _basename_and_extension(filename):
        parts = os.path.basename(filename).rsplit('.', 1)
        if len(parts) > 1:
            return parts
        else:
            return parts, None
