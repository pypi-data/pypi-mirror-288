from rich.console import Console
from rich import print as rprint
from time import sleep

console = Console()


def hack():
	with console.status('Hacking the Pentagon'):
		sleep(5)
		rprint("[bold green]\nSuccessfully!")
