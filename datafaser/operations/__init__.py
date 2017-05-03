from datafaser.operations.load import Loader
from datafaser.operations import table


def get_default_operations_map(data_tree):
    return {
        'load': Loader(data_tree).load,
        'table': table.convert
    }
