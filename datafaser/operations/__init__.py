from datafaser.operations import table, change, load


def get_default_operations_map(data_tree):
    return {
        'load': load.Loader(data_tree).load,
        'table': table.convert,
        'change': change.map_keys
    }
