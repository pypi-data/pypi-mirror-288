import git
from rich import print

from datazone.utils.helpers import check_datazone_repo


def pull() -> None:
    check_datazone_repo()

    repo = git.Repo()
    origin = repo.remotes.origin

    origin.pull()
    print("[green]Repository is up to date.[/green]:rocket:")
