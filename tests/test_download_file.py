from pathlib import Path

from src.get_exe_path import GetExePath


class TestDownloadFile:

    def test_no_download(self):
        status, msg = GetExePath('7z').download_file()
        assert not status
        assert msg == "Path to software not found and automatic download not enabled."
        status, msg = GetExePath('7z', download=False).download_file()
        assert not status
        assert msg == "Path to software not found and automatic download not enabled."

    def test_download(self):
        status, msg = GetExePath('7z', download=True).download_file()
        assert status
        assert msg.exists() and msg.is_file()
        print(f"Download path: {msg}")
        download_path = Path('./downloads/7z/')
        status, msg = GetExePath('7z', download=True, download_path=download_path).download_file()
        assert status
        assert msg.exists() and msg.is_file()
        print(f"Download path: {msg}")
