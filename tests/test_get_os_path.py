import os

import pytest

from src.get_exe_path import GetExePath


class TestGetOSPath:

    @pytest.fixture(autouse=True)
    def get_path(self):
        return GetExePath('7z')

    def test_from_path(self, get_path):
        os.environ['PATH'] = 'C:\\Program Files\\7-Zip'
        path = get_path.get_os_path()
        assert path is not None
        print(path)
        assert path.exists() and path.is_file()

    def test_from_name_env(self, get_path):
        os.environ['7Z_PATH'] = 'C:\\Program Files\\7-Zip'
        path = get_path.get_os_path()
        assert path is not None
        print(path)
        assert path.exists() and path.is_file()
