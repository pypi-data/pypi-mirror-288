import os
from pathlib import Path
from typing import Optional, Iterator
from git import Repo, InvalidGitRepositoryError
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ai_commit.config import TomlConfigRepository, ConfigService, default_config_file_path, AppConfig

user_template = """
The git diff is below.

{diff}
"""


def check_api_key() -> None:
    """
    Checks if the OpenAI API key is set in the environment variables.

    Raises:
        ValueError: If the API key is not set.
    """
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OpenAI API key not set")


def find_git_root(path: Path) -> Path:
    """
    Recursively finds the root directory of a Git repository.

    Args:
        path (Path): The starting path to search for the Git root.

    Returns:
        Path: The path to the Git root directory.

    Raises:
        FileNotFoundError: If the Git root directory is not found.
    """
    if (path / ".git").exists():
        return path
    if path == path.parent:
        raise FileNotFoundError("Git root not found")
    return find_git_root(path.parent)


def get_git_change(repo: Repo) -> Optional[str]:
    """
    Retrieves the current changes in the Git repository.

    Args:
        repo (Repo): The Git repository object.

    Returns:
        Optional[str]: The diff of the staged changes if present, otherwise the diff of the unstaged changes.
                       Returns None if no changes are found.
    """
    if repo.bare:
        raise ValueError("Cannot get changes from a bare repository")

    staged_change = repo.git.diff("--staged")

    if staged_change:
        return staged_change
    else:
        unstaged_change = repo.git.diff()
        if unstaged_change:
            return unstaged_change
        else:
            return None


def generate_commit_message(model: str, prompt: str) -> Iterator[BaseMessage] | None:
    """
    Generates a commit message based on the user's changes.

    Returns:
        str: The generated commit message.
    """
    try:
        repo = Repo(find_git_root(Path.cwd()))
    except FileNotFoundError:
        raise
    except InvalidGitRepositoryError:
        raise ValueError("Invalid Git repository")

    diff = get_git_change(repo)
    if diff is None:
        return None

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("user", user_template),
        ]
    )

    model = ChatOpenAI(model=model)
    chain = prompt_template | model

    return chain.stream({"diff": diff})


def print_message(messages: Iterator[BaseMessage]):
    for message in messages:
        print(message.content, end="")


def main():
    config_service = ConfigService(TomlConfigRepository(default_config_file_path()))
    config: AppConfig = config_service.get_config()

    check_api_key()

    result = generate_commit_message(config.model, config.prompt)

    if result is not None:
        print_message(result)

    print()


if __name__ == '__main__':
    main()
