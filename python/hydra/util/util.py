'''
    utility methods
'''

def is_subset(subset, set):
    if (not isinstance(subset, list) and not isinstance(subset, tuple)) or (not isinstance(set, list) and not isinstance(set, tuple)):
        return False

    for obj in subset:
        if not obj in set:
            return False

    return True