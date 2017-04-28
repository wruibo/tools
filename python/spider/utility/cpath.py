'''
    path, dir, file tools
'''
import os

def is_file(path):
    return os.path.isfile(path)

def file_name(path):
    return os.path.basename(path)

def dir_name(path):
    return path.rstrip().rstrip('/').split('/')[-1]

def join_paths(path, *paths):
    '''
        join subpaths with path to a complate path,example:
        path1, path2, file
        path1, /path2, file
        path1/, /path2/, file
        ->
        path1/path2/file
    :param path: path to be joined with subpaths
    :param paths: paths to be join
    :return: string, joined path
    '''
    path = path.rstrip().rstrip('/')
    for spath in paths:
        spath = spath.lstrip().lstrip('/')
        spath = spath.rstrip().rstrip('/')
        path = path + "/" + spath

    return path


def norm_path(path):
    return os.path.normpath(path)


def path_exists(path):
    return os.path.exists(path)


def is_absolute_path(path):
    '''
    detect whether @path is an absolute path, like: /tmp/abc, /lib/abc, ...
    :param uri: string, path to detect
    :return: boolean
    '''
    return os.path.isabs(path)


def is_relative_path(path):
    '''
        detect whether @path is an relative path, like: tmp/abc, lib/abc, ....
    :param uri: string, path to detect
    :return: boolean
    '''
    return not is_absolute_path(path)


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def remove_dir(path):
    if os.path.exists(path):
        subpaths = os.listdir(path)
        for subpath in subpaths:
            abspath = "%s/%s" % (path, subpath)
            if os.path.isfile(abspath):
                os.remove(abspath)
            else:
                remove_dir(abspath)

        os.rmdir(path)

def remove_dirs(*paths):
    for path in paths:
        remove_dir(path)

def remove_file(file):
    if os.path.isfile(file):
        os.remove(file)

def remove_files(*files):
    for file in files:
        os.remove(file)

def rename(src, dst):
    os.rename(src, dst)

def renames(old, new):
    os.renames(old, new)

def move(src, dst):
    os.rename(src, dst)

def moves(old, new):
    os.renames(old, new)

def list_dirs(path, onlyname=True):
    dpaths = []

    names = os.listdir(path)
    if onlyname:
        for name in names:
            dpath = os.path.join(path, name)
            if not os.path.isfile(dpath):
                dpaths.append(name)
    else:
        for name in names:
            dpath = os.path.join(path, name)
            if not os.path.isfile(dpath):
                dpaths.append(dpath)

    return dpaths

def list_files(path, onlyname=True):
    fpaths = []

    names = os.listdir(path)
    if onlyname:
        for name in names:
            fpath = os.path.join(path, name)
            if os.path.isfile(fpath):
                fpaths.append(name)
    else:
        for name in names:
            fpath = os.path.join(path, name)
            if os.path.isfile(fpath):
                fpaths.append(fpath)

    return fpaths


if __name__ == "__main__":
    print join_paths('/path1/', '/path2/', 'file')
    print is_relative_path("path/")
    print list_files('/tmp')
    print list_dirs('/tmp')
