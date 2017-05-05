'''
    utility methods
'''

def is_subset(subset, set):
    if not isinstance(subset, list) or not isinstance(subset, tuple) or not isinstance(set, list) or not isinstance(set, tuple):
        return False

    for obj in subset:
        if not obj in set:
            return False

    return True