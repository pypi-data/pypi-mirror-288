import requests

from datetime import datetime
from pathlib import Path
from git import Repo

from ..lib.config import Config
from ..lib.enums import Messages


class Git:
    def __init__(self, server: str) -> None:
        self.server = server
        self.path = Path()
        if self.repo_exists():
            self.repo = self.get_repo()
        else:
            self.repo = self.create_repo()
            self.init_remote_repo()

        if not self.repo.remotes:
            self.repo.create_remote('origin', Config.SERVER_GIT_ORIGIN.format(version=self.server))

    def get_repo(self):
        return Repo(self.path)

    def create_repo(self):
        return Repo.init(self.path)

    def repo_exists(self) -> bool:
        return bool([x for x in self.path.iterdir() if x.is_dir() and x.name == '.git'])

    def init_remote_repo(self):
        requests.post(
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {Config.PERSONAL_ACCESS_TOKEN}"
            },
            url='https://api.github.com/orgs/MinecraftModServers/repos',
            json={
                "name": self.server
            }
        )

    def get_diffs(self):
        return [x.a_path for x in self.repo.index.diff(None)]

    def save(self) -> str:
        to_add = self.repo.untracked_files + self.get_diffs()
        if not to_add:
            return Messages.ALREADY_UPDATED.value
        self.repo.git.add(self.repo.untracked_files + self.get_diffs())
        self.repo.git.commit(m=f"save world {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.repo.git.push('--set-upstream', self.repo.remote().name, 'main')

        return Messages.UPDATED.value

    def get_updates(self):
        self.repo.git.pull(self.repo.remote().name, 'main')

    @staticmethod
    def clone(server):
        return Repo.clone_from(Config.SERVER_GIT_ORIGIN.format(version=server), Path(server))
