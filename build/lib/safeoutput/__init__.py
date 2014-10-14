from os import rename
from os.path import abspath, dirname
from sys import stdout
from tempfile import NamedTemporaryFile

class SafeOutput:
  def __init__(self, dst=None):
    self.dst = dst

  def __getattr__(self, name):
    # Attribute lookups are delegated to the underlying tempfile
    fd = self.__dict__['fd']
    a = getattr(fd, name)
    return a

  def __enter__(self):
    if self.dst is None:
      self.fd = stdout
    else:
      self.fd = NamedTemporaryFile(dir=dirname(abspath(self.dst)))
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_value is None:
      if self.dst is not None:
        # Try to commit the file.
        rename(self.fd.name, self.dst)
        self.fd.delete = False
    return self.fd.__exit__(exc_type, exc_value, traceback)

