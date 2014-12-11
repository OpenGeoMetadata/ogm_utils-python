__author__ = 'cbarne02'
"""
Uses the FNV-1a hashcode on the layerid to attempt to distribute files evenly across
directories.

more info <http://www.isthe.com/chongo/tech/comp/fnv/>

thanks to vaiorabbit:
<https://gist.github.com/vaiorabbit/5670985>
for a python implementation of the FNV-1a hash

"""
import os
import errno


def get_directory(file_id, base_path):
    path = get_hash_dir(file_id)
    path = os.path.join(base_path, path)
    mkdir_p(path)
    chk_dir(path)
    return path


def fnv32a( str ):
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in str:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return hval


def get_hash_tuple(string):
    hashcode = fnv32a(string)
    mask = 255
    dir_1 = hashcode & mask
    dir_2 = hashcode >> 8 & mask
    dir_3 = hashcode >> 16 & mask
    dir_4 = hashcode >> 24 & mask

    return dir_1, dir_2, dir_3, dir_4


def get_hash_dir(string, levels = 4):
    tup = get_hash_tuple(string)
    path = ""
    while levels > 0:
        if len(path) > 0:
            path = os.path.join(str(tup[levels - 1]), path)
        else:
            path = str(tup[levels - 1])
        levels -= 1
    return path


def chk_dir(path):
    ok = False
    try:
        ok = os.access(path, os.W_OK) and os.access(path, os.X_OK)
    except TypeError as e:
        print "type error"

    if not ok:
        raise OSError("This directory is not writable!")


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise OSError("Problem creating directories!")


def dir_size(path):
    return len(os.listdir(path))

