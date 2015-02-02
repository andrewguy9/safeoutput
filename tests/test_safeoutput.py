import safeoutput
from os.path import isfile
from os import remove
import pytest

def ensure_file_absent(path):
  try:
    remove(path)
  except OSError:
    pass

def expected_file(path, expected):
  if expected is not None:
    with open(path, 'r') as f:
      content = f.read()
      return content == expected
  else:
    return False == isfile(path)

def test_with_success():
  file_name = "testfile"
  file_data = "testoutput"
  ensure_file_absent(file_name)
  with safeoutput.open(file_name) as f:
    f.write(file_data)
  assert expected_file(file_name, file_data)


def test_with_exception():
  file_name = "testfile"
  file_data = "testoutput"
  ensure_file_absent(file_name)
  try:
    with safeoutput.open(file_name) as f:
      f.write(file_data)
      raise ValueError("We eff'ed up")
  except ValueError:
    pass
  assert expected_file(file_name, None)

def test_close_success():
  file_name = "testfile"
  file_data = "testoutput"
  ensure_file_absent(file_name)
  f = safeoutput.open(file_name)
  f.write(file_data)
  f.close()
  assert expected_file(file_name, file_data)


def test_close_exception():
  file_name = "testfile"
  file_data = "testoutput"
  ensure_file_absent(file_name)
  def write():
    f = safeoutput.open(file_name)
    f.write(file_data)
    raise ValueError("We eff'ed up")
  try:
    write()
  except ValueError:
    pass
  assert expected_file(file_name, None)

def test_write_after_close():
  file_name = "testfile"
  file_data = "testoutput"
  ensure_file_absent(file_name)
  f = safeoutput.open(file_name)
  f.write(file_data)
  f.close()
  assert expected_file(file_name, file_data)
  with pytest.raises(ValueError):
    f.write(file_data)
  assert expected_file(file_name, file_data)

