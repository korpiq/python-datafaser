from datafaser.operations.load import Loader


def get_default_operations_map(data_tree):
    return {
        'load': Loader(data_tree).load
    }
