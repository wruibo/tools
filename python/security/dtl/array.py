"""
    array definition
"""


def create(*args):
    """
        create an array object
    :param args:
    :return:
    """
    return Array(*args)


def array(mtx):
    """
        change the multi-dimension array @mtx to one-dimension, e.g.:
    input:
        [
            [1, 2, 3],
            [4, 5, 6],
            [[7], [8], [9, 10]]
        ]
    output:
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    :param mtx: list, multi dimension array
    :return: list, one dimension array
    """
    if not (isinstance(mtx, list) or isinstance(mtx, tuple)):
        return [mtx]

    results = []

    for elm in mtx:
        if isinstance(mtx, list) or isinstance(mtx, tuple):
            results.extend(array(elm))
        else:
            results.append(elm)

    return results


class Array(list):
    """
        array class
    """
    def __init__(self, *args):
        if len(args) == 1 and (isinstance(args[0], tuple) or isinstance(args[0], list)):
            super(Array, self).__init__(args[0])
        else:
            super(Array, self).__init__(args)
