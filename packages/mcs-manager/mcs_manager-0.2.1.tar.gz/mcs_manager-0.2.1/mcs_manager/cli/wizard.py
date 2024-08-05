import os
import signal
import subprocess

from pathlib import Path
from pyngrok import conf, ngrok
from InquirerPy import inquirer

from ..lib.client import DownloadServer
from ..lib.server import Server
from ..lib.config import Config
from ..lib.git import Git


class Wizzard:
    @staticmethod
    def create():
        versions_list = list(map(lambda value: value['version'], DownloadServer().list()))
        return {
            "type": inquirer.select(
                message='Select a server type:',
                default='forge',
                choices=['forge'],
                validate=lambda v: len(v) > 0,
            ).execute(),
            "version": inquirer.select(
                message='Select one version:',
                choices=versions_list,
                validate=lambda v: len(v) > 0,
            ).execute(),
            "confirm": inquirer.confirm(
                message='Confirm:'
            ).execute()
        }

    @staticmethod
    def select_server_existing_to_init():
        return {
            "server": inquirer.select(
                message='Select the server to initialize:',
                choices=Server.get_folders(),
                validate=lambda v: len(v) > 0,
            ).execute()
        }

    @staticmethod
    def select_server_existing_in_git():
        return {
            "server": inquirer.select(
                message='Select the server to pull:',
                choices=Server.get_available_servers_into_git(),
                validate=lambda v: len(v) > 0,
            ).execute()
        }

    @staticmethod
    def install(server: str):
        previous_path = Path.cwd()
        os.chdir(server)

        try:
            subprocess.call(
                Config.COMMAND_INSTALL,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
        except KeyboardInterrupt:
            print("Exiting...")

        os.chdir(previous_path)

    @staticmethod
    def first_start(server: str):
        previous_path = Path.cwd()
        os.chdir(server)

        executable = Server.get_server_executable()

        try:
            subprocess.check_call(
                Config.COMMAND_START.format(executable=executable),
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as exc:
            print(exc)
        os.chdir(previous_path)

    @staticmethod
    def eula(server: str):
        previous_path = Path.cwd()
        os.chdir(server)

        with open(Server.get_eula(), 'r+') as file:
            text = file.read().replace('false', 'true')
            file.truncate(0)
            file.seek(0)
            file.write(text)

        os.chdir(previous_path)

    @staticmethod
    def ngrok():
        if not conf.get_default().auth_token:
            ngrok.set_auth_token(Config.NGROK_TOKEN)

        return ngrok.connect(Config.PORT, "tcp")

    @staticmethod
    def stop_ngrok(public_url: str):
        ngrok.disconnect(public_url)

    @staticmethod
    def start(server: str):
        previous_path = Path.cwd()
        os.chdir(server)

        executable = Server.get_server_executable()

        try:
            subprocess.run(
                Config.COMMAND_START.format(executable=executable),
                shell=True,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        except KeyboardInterrupt:
            os.kill(Server.get_server_pid(), signal.SIGKILL)
        except Exception as exc:
            print(exc)

        os.chdir(previous_path)

    @staticmethod
    def save(server: str):
        previous_path = Path.cwd()
        os.chdir(server)

        git = Git(server=server)
        message = git.save()

        os.chdir(previous_path)
        return message

    @staticmethod
    def clone(server: str):
        Git.clone(server=server)
