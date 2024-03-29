import argparse
import logging
import sys
from builtins import object
from os import rename
from os.path import abspath, dirname
from tempfile import NamedTemporaryFile

LOG = logging.getLogger(__name__)

def _sameDir(dst):
    return dirname(abspath(dst))

def open(dst=None, mode="w", useDir=_sameDir):
    if dst:
        fd = NamedTemporaryFile(dir=useDir(dst), mode=mode)
    else:
        if mode == "w":
            fd = sys.stdout
        else:
            try:
                fd = sys.stdout.buffer
            except AttributeError:
                fd = sys.stdout
    return _SafeOutputWrapper(fd, dst)


class _SafeOutputWrapper(object):

    def __init__(self, fd, dst):
        self.fd = fd
        self.dst = dst

    def __enter__(self):
        if self.dst:
            self.fd.__enter__()
        return self

    def __getattr__(self, name):
        # Attribute lookups are delegated to the underlying tempfile
        fd = self.__dict__['fd']
        a = getattr(fd, name)
        return a

    def close(self, commit=True):
        if self.dst:
            if commit == True:
                LOG.debug(u"renaming %s to %s", self.fd.name, self.dst)
                self.fd.flush()
                rename(self.fd.name, self.dst)
                # self.fd.delete = False # doesn't work in python3...?
            try:
                LOG.debug(u"closed %s", self.fd.name)
                self.fd.close()
            except EnvironmentError:  # aka FileNotFoundError in Python 3
                pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close(exc_value is None)
        if self.dst:
            return self.fd.__exit__(exc_type, exc_value, traceback)
        else:
            return exc_type == None

    def __del__(self):
        # If we get to __del__ and have not already committed,
        # we don't know that the output is safe. Allow
        # tempfile to delete the file.
        self.close(False)


def main(args=None):
    """Buffer stdin and flush, and avoid incomplete files."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--binary',
                        dest='mode',
                        action='store_const',
                        const="wb",
                        default="w",
                        help='write in binary mode')
    parser.add_argument('output',
                        metavar='FILE',
                        type=unicode,
                        help='Output file')

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stderr,
        format='[%(levelname)s elapsed=%(relativeCreated)dms] %(message)s')

    args = parser.parse_args(args or sys.argv[1:])

    with open(args.output, args.mode) as fd:
        for line in sys.stdin:
            fd.write(line)
