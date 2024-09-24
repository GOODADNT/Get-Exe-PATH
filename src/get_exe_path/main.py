import hashlib
import os
from pathlib import Path

import httpx

from . import utils


class GetExePath:

    def __init__(self, name: str,
                 download: bool = False,
                 download_url: str = '',
                 download_path: str | Path = '',
                 file_name: str = '',
                 val_type: str = 'sha256',
                 val_url: str = ''):
        self.name = name
        self.download = download
        self.download_url = download_url
        self.download_path = download_path
        self.file_name = file_name
        self.val_type = val_type
        self.val_url = val_url

        self.save_path = ''

        status, msg = self._check_url()
        if not status:
            raise ValueError(msg)

    def get_path(self) -> tuple[bool, Path | str]:
        exe_path = self.get_os_path()
        if exe_path is not None:
            return True, exe_path
        return self.download_file()

    def get_os_path(self) -> Path | None:
        env_vars = os.environ
        path_vars = env_vars.get('PATH')
        if path_vars is not None:
            for path in path_vars.split(os.pathsep):
                path = Path(path) / f'{self.name}.exe'
                if path.exists():
                    return path

        env_path = env_vars.get(f'{self.name.upper()}_PATH')
        if env_path is not None:
            path = Path(env_path).resolve()
            path = path / f'{self.name}.exe'
            if path.exists():
                return path
        return None

    def download_file(self) -> tuple[bool, Path | str]:
        if not self.download:
            return False, "Path to software not found and automatic download not enabled."

        if self.download_path == '':
            downloads_path = Path.home() / "Downloads"
            self.download_path = downloads_path / self.name
        elif isinstance(self.download_path, str):
            self.download_path = Path(self.download_path).resolve()

        if self.file_name == '':
            self.file_name = self.download_url.split('/')[-1]
        save_path = self.download_path / self.file_name

        try:
            if not self.val_file(save_path):
                self.download_path.mkdir(parents=True, exist_ok=True)
                with httpx.stream("GET", self.download_url, follow_redirects=True) as response:
                    if response.status_code != 200:
                        return False, "Failed to download."
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_bytes():
                            f.write(chunk)
        except PermissionError:
            return False, "Insufficient file or directory operating privileges."
        except httpx.ConnectTimeout:
            return False, "Failed to download."
        return True, save_path

    def val_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            return False
        if self.val_url == '':
            self.val_url = utils.val_url.get(self.name)
        if self.val_url is not None:
            try:
                val_str = httpx.get(self.val_url, follow_redirects=True)
                val_str = val_str.text
            except httpx.RequestError:
                return False
            with open(file_path, 'rb') as f:
                hash_calc = hashlib.new(self.val_type)
                while chunk := f.read(8192):
                    hash_calc.update(chunk)
            return hash_calc.hexdigest() == val_str
        else:
            try:
                val_size = httpx.head(self.download_url, follow_redirects=True).headers.get('Content-Length')
                if val_size is None:
                    return False
                val_size = int(val_size)
            except httpx.ConnectTimeout:
                return False
            return file_path.stat().st_size == val_size

    def _check_url(self):
        if self.download_url == '':
            self.download_url = utils.download_url.get(self.name)
        if self.download_url is None:
            return False, "The download link is not provided and the software name is not found in the configuration."
        return True, "Download link is valid."
