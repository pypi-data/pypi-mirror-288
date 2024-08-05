import re
import psutil
from pathlib import Path

import requests

from .config import Config


class Server:
    @staticmethod
    def get_folders():
        return [str(folder) for folder in Path().iterdir() if folder.is_dir() and folder.match(r'[0-9]*.[0-9]*.[0-9]*')]

    @staticmethod
    def get_server_executable():
        return [str(folder) for folder in Path().iterdir() if folder.is_file() and folder.match(r'forge-*.jar')][0]

    @staticmethod
    def get_files():
        return list(Path().iterdir())

    @staticmethod
    def get_server_pid():
        java_processes = [proc for proc in psutil.process_iter() if proc.name() == 'java']

        for proc in java_processes:
            for c in proc.connections():
                if c.status == 'LISTEN' and c.laddr.port == Config.PORT:
                    return proc.pid

    @staticmethod
    def get_eula():
        if Path('eula.txt').is_file():
            return Path('eula.txt')

    @staticmethod
    def get_available_servers_into_git():
        response = requests.get(
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {Config.PERSONAL_ACCESS_TOKEN}"
            },
            url='https://api.github.com/orgs/MinecraftModServers/repos',
        ).json()

        servers = list(map(lambda server: server['name'], response))

        p = re.compile(r'^[0-9]*.[0-9]*.[0-9]*$')
        return [x for x in servers if p.match(x)]
