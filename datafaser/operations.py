from datafaser.data import Data
from datafaser.files import FileLoader, FileSaver


def get_default_operations_map():
    return {
        'load': load
    }


def load(data, directives):
    new_data = Data({})

    if 'from' in directives:
        for source in directives['from']:
            if 'files' in source:
                if not isinstance(source, dict):
                    raise TypeError('Not a dict: %s: "%s"' % (type(source), source))
                FileLoader(new_data).load(source['files'])
            if 'data' in source:
                for key in source['data']:
                    new_data.merge(data.dig(key))

    if 'to' in directives:
        save(data, new_data, directives['to'])
    else:
        data.merge(new_data.data)


def save(data, new_data, targets):
    for target in targets:
        if 'data' in target:
            data.merge(new_data.data, target['data'])
        if 'files' in target:
            writer = FileSaver(new_data.data)
            for output_format, filename in target['files'].items():
                writer.save(filename, output_format)
