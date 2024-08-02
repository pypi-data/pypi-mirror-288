import git
from rich import print

from datazone.constants import Constants
from datazone.service_callers.crud import CrudServiceCaller
from datazone.service_callers.datazone import DatazoneServiceCaller


def initialize_git_repo(project_id: str) -> None:
    repository_session = CrudServiceCaller(entity_name="repository-session").create_entity(
        payload={"project": project_id},
    )
    token = repository_session.get("token")

    git_url = f"{DatazoneServiceCaller.get_service_url()}/git/{token}"

    repo = git.Repo.init()
    print("[green]Repository has initialized[/green]")

    origin = repo.create_remote("origin", git_url)

    origin.fetch()
    repo.git.checkout(Constants.DEFAULT_BRANCH_NAME)
    origin.pull()


def is_git_repo():
    try:
        _ = git.Repo()
    except git.exc.InvalidGitRepositoryError:
        return False
    else:
        return True
