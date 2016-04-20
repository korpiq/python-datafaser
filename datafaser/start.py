"""
Builds first run plan to load files given as arguments.
"""

from datafaser.data_tree import DataTree
from datafaser.run import Runner
from datafaser import formats


def create_runner_to_load(files):
    """
    :param files: list of paths to files or directories to load as data
    :return: datafaser.run.Runner configured to load given files
    """

    return Runner(DataTree(create_plan_to_load_files(files)))


def create_plan_to_load_files(files):
    """
    :param files: list of paths to files or directories to load as data
    :return: data structure containing plan to load files given as arguments
    """

    return {
        'datafaser': {
            'run': {
                'arguments': files,
                'plan': [get_load_phase_for_files(files)],
                'done': []
            },
            'formats': formats.default_settings
        }
    }


def get_load_phase_for_files(files):
    """
    :param files: list of paths to files or directories to load as data
    :return: data structure containing run plan phase to load files given as arguments
    """

    return {'start': [{
        'load': {
            'from': [{
                'files': files
            }]
        }
    }]}
