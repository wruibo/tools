"""
    file and directory operation methods
"""
import os



def candidate_tempdirs():
    """
        get the candidate temporary directories
    :return: list, directories paths
    """
    dirs = []
    if os.name == "nt":
        dirs.extend([r'c:/temp', r'c:/tmp'])
    else:
        dirs.extend(['/tmp', '/var/tmp'])

    for env in ['TMPDIR', 'TMP', 'TEMP']:
        path = os.getenv(env)
        if path is not None: dirs.append(path)

    return dirs


def tempdir():
    """
        get temp directory
    :return: str, temp directory
    """
    for dir in candidate_tempdirs():
        if os.path.exists(dir) and os.access(dir, os.X_OK|os.W_OK|os.R_OK):
            return dir

    raise "no usable temporary directory."
