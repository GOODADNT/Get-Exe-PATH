import os

from src.get_exe_path import GetExePath


class TestGetPath:

    def test_exists_env(self):
        get_path = GetExePath('7z')
        os.environ['7Z_PATH'] = 'C:\\Program Files\\7-Zip'
        status, path = get_path.get_path()
        assert status
        assert path.exists() and path.is_file()
        print(path)

    def test_not_exists_env_no_download(self):
        get_path = GetExePath('test', download=True, file_name='test')
        path = get_path.get_os_path()
        if path is not None:
            os.environ.pop('TEST_PATH', None)
            os.environ.pop('PATH', None)
        path = get_path.get_os_path()
        assert path is None
        status, path = get_path.get_path()
        print(path)
        assert status
        assert path.exists() and path.is_file()
