import os
import errno


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


def force_padding(s, pad):
    if not s.startswith(pad):
        s = pad + s
    if not s.endswith(pad):
        s = s + pad
    return s
