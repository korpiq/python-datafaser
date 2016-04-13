from datafaser.data import Data
from datafaser.files import FileLoader, FileSaver


class Runner:

    class Operations:

        @staticmethod
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
                for target in directives['to']:
                    if 'data' in target:
                        data.merge(new_data.data, target['data'])
                    if 'files' in target:
                        writer = FileSaver(new_data.data)
                        for output_format, filename in target['files'].items():
                            writer.save(filename, output_format)
            else:
                data.merge(new_data.data)

    operations = {
        'load': Operations.load
    }

    def __init__(self, data, operations=None):
        """
        :param data: datafaser.data.Data object
        :param operations: map to operation names to functions implementing them
        """

        self.data = data
        if operations:
            self.operations = operations

    def run(self, plan):
        """
        :param plan: list of phases: a phase is a map from operation name to its parameter structure.
        """

        for phase in plan:
            for operation in phase.keys():
                if operation in self.operations:
                    self.operations[operation](self.data, phase[operation])
                else:
                    raise ValueError('Unknown operation: "%s"' % operation)
