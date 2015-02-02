from safeoutput import SafeOutputFile
from os.path import isfile

def expected_file(path, expected):
  if expected is not None:
    with open(path, 'r') as f:
      content = f.read()
      return content == expected
  else:
    return False == isfile(path)

def test_success():
  file_name = "testfile"
  file_data = "testoutput"
  with SafeOutputFile(file_name) as f:
    f.write(file_data)
  assert expected_file(file_name, file_data)


def test_exception():
  file_name = "testfile"
  file_data = "testoutput"
  try:
    with SafeOutputFile(file_name) as f:
      f.write(file_data)
      raise ValueError("We eff'ed up")
  except ValueError:
    pass
  assert expected_file(file_name, file_data)

