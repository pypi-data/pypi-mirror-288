import typer

from rich.console import Console

from ..cli.wizard import Wizzard
from ..lib.client import DownloadServer
from ..lib.enums import Messages
from ..lib.git import Git


command_app = typer.Typer(help=__doc__)
console = Console()


@command_app.command(help='Download and create an empty minecraft server')
def download():
    console.rule("Create a Minecraft Server")

    response = Wizzard.create()

    if not response['confirm']:
        console.print(f"\n[red]Exit![/]")
        return

    with console.status('[yellow]Please wait...'):
        DownloadServer().download(version=response['version'])
        console.print('Download completed!')
    

    console.print(f"\n[green]Success![/] Minecraft Server version `{response['version']}` created.")
    console.print(f"\nNow type: [bold]python main.py init[/]")
    console.rule()


@command_app.command(help='Initialize the empty minecraft server downloaded. Use after `download` command!')
def init():
    console.rule("Initialize Server")

    response = Wizzard.select_server_existing_to_init()

    with console.status('[yellow]Downloading... This may take a few minutes.'):
        Wizzard.install(server=response['server'])

    with console.status('[yellow]First start and editing EULA...'):
        Wizzard.first_start(server=response['server'])
        Wizzard.eula(server=response['server'])
    
    console.print(f"\n[green]Success![/] Finished.")
    console.print(f"\nNow type: [bold]python main.py start[/]")


@command_app.command(help='Choice and start a Minecraft Server by version')
def start():
    console.rule("Start Server")

    response = Wizzard.select_server_existing_to_init()

    with console.status('[yellow]Checking updates...'):
        Git(server=response['server']).get_updates()
        console.print(f"\n[green bold]Success![/] Your server is up to dated!")

    server = Wizzard.ngrok()

    console.print(f'\n[green bold]Server URL:[/] [bold]{server.public_url}')

    Wizzard.start(server=response['server'])
    Wizzard.stop_ngrok(server.public_url)

    with console.status('[yellow]Saving your world in GitHub... This may take a few minutes.'):
        message = Wizzard.save(server=response['server'])

    if message == Messages.ALREADY_UPDATED.value:
        console.print(f"\n[green bold]Don't care![/] Your server is already up to dated!")
    if message == Messages.UPDATED.value:
        console.print(f"\n[green bold]Success![/] Your server is saved!")

    console.rule(f"\nServer closed")


@command_app.command(help='Choice and save in Cloud your server.')
def save():
    console.rule("Save Server")

    response = Wizzard.select_server_existing_to_init()

    with console.status('[yellow]Saving your world in GitHub... This may take a few minutes.'):
        message = Wizzard.save(server=response['server'])

    if message == Messages.ALREADY_UPDATED.value:
        console.print(f"\n[green bold]Don't care![/] Your server is already up to dated!")
    if message == Messages.UPDATED.value:
        console.print(f"\n[green bold]Success![/] Your server is saved!")


@command_app.command(help='Get an existent Minecraft Server available in GitHub Organization.')
def clone():
    console.rule("Clone Server")

    response = Wizzard.select_server_existing_in_git()

    with console.status('[yellow]Cloning your server from GitHub... This may take a few minutes.'):
        Wizzard.clone(server=response['server'])
    
    console.print(f"\n[green bold]Success![/] Your server is ready!")
    console.print(f"\nNow type: [bold]python main.py start[/]")
