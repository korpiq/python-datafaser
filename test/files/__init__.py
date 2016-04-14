import os


def path_to_test_data(*parts):
    """
    Turn a list of strings into a list with correct file path string that is a combination of them.

    :param parts: string directory names optionally ending in a filename
    :return: list containing correct file path
    """
    return [os.path.join('test', 'test_data', *parts)]
