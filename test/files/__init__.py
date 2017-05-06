import os


def path_to_test_data(*parts):
    """
    Turn a list of strings into a string with correct file path string that is a combination of them.

    :param parts: string directory names optionally ending in a filename
    :return: string containing correct file path
    """
    return os.path.join('test', 'test_data', *parts)
