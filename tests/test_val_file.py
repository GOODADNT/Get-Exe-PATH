from pathlib import Path

import pytest

from src.get_exe_path import GetExePath


class TestValFile:

    @pytest.fixture(autouse=True)
    def get_path(self):
        return GetExePath('7z')

    def test_no_file(self, get_path):
        no_file_path = Path('./downloads/7z2408-x64.exe')
        no_file = get_path.val_file(no_file_path)
        assert not no_file

    def test_exist_url(self, get_path):
        get_path.name = 'ffmpeg'
        file_path = Path('./downloads/ffmpeg-release-full.7z')
        exist_file = get_path.val_file(file_path)
        assert exist_file

    def test_no_url(self, get_path):
        get_path.name = '7z'
        file_path = Path('./downloads/7z/7z2408-x64.exe')
        exist_file = get_path.val_file(file_path)
        assert exist_file
