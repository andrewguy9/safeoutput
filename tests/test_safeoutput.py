import inspect
from os import remove
from os.path import isfile

import pytest
import safeoutput


def _filename():
    return u"testfile_" + inspect.stack()[1][3]


def ensure_file_absent(path):
    try:
        remove(path)
    except OSError:
        pass


def expected_file(path, expected, cleanup=True):
    try:
        if expected is not None:
            with open(path, 'r') as f:
                content = f.read()
                return content == expected
        else:
            return False == isfile(path)
    finally:
        if cleanup:
            ensure_file_absent(path)


def test_with_success():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    with safeoutput.open(file_name) as f:
        f.write(file_data)
    assert expected_file(file_name, file_data)


def test_with_exception():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
            raise ValueError(u"We eff'ed up")
    except ValueError:
        pass
    assert expected_file(file_name, None)


def test_close_success():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    f = safeoutput.open(file_name)
    f.write(file_data)
    f.close()
    assert expected_file(file_name, file_data)


def test_close_exception():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)

    def write():
        f = safeoutput.open(file_name)
        f.write(file_data)
        raise ValueError(u"We eff'ed up")

    try:
        write()
    except ValueError:
        pass
    assert expected_file(file_name, None)


def test_write_after_close():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    f = safeoutput.open(file_name)
    f.write(file_data)
    f.close()
    assert expected_file(file_name, file_data, False)
    with pytest.raises(ValueError):
        f.write(file_data)
    assert expected_file(file_name, file_data)
