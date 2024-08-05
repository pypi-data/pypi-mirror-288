import os
from typing import List

import requests


class DownloadServer:
    def __init__(self, type: str = 'forge') -> None:
        self.type = type

    def list(self) -> List[dict]:
        response = requests.get(url=f'https://mcutils.com/api/server-jars/{self.type}')
        return response.json()

    def download(self, version: str):
        response = requests.get(url=f'https://mcutils.com/api/server-jars/{self.type}/{version}/download')
        os.makedirs(version, exist_ok=True)
        open(f'{version}/server.jar', 'wb').write(response.content)
