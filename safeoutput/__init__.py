from os import rename
from os.path import abspath, dirname
from sys import stdout
from tempfile import NamedTemporaryFile


def open(dst=None):
  if dst:
    fd = NamedTemporaryFile(dir=dirname(abspath(dst)))
  else:
    fd = stdout
  return _SafeOutputWrapper(fd, dst)

class _SafeOutputWrapper:
  def __init__(self, fd, dst):
    self.fd = fd
    self.dst = dst

  def rename(self, dst):
    self.dst = dst

  def __enter__(self):
    self.fd.__enter__()
    return self

  def __getattr__(self, name):
    # Attribute lookups are delegated to the underlying tempfile
    fd = self.__dict__['fd']
    a = getattr(fd, name)
    return a

  def close(self, commit=True):
    if self.dst is not None and commit == True:
      rename(self.fd.name, self.dst)
      self.fd.delete = False
    self.dst = None
    self.fd.close()

  def __exit__(self, exc_type, exc_value, traceback):
    self.close(exc_value is None)
    return self.fd.__exit__(exc_type, exc_value, traceback)

  def __del__(self):
    # If we get to __del__ and have not already committed,
    # we don't know that the output is safe. Allow
    # tempfile to delete the file.
    self.close(False)
