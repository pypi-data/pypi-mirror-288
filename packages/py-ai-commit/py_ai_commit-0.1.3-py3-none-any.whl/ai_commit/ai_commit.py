import os
from pathlib import Path
from typing import Optional, Iterator
from git import Repo, InvalidGitRepositoryError
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

ai_model = "gpt-4o-mini"

system_template = """
You are an AI assistant tasked with generating commit messages that strictly adhere to the commitizen conventions. Please follow these instructions to create commit messages:

1. Select the type of commit from the following options:
   - feat: A new feature
   - fix: A bug fix
   - docs: Documentation only changes
   - style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
   - refactor: A code change that neither fixes a bug nor adds a feature
   - perf: A code change that improves performance
   - test: Adding missing tests or correcting existing tests
   - chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

2. Specify the scope of the change (optional). This can help clarify which part of the codebase is affected.

3. Write a short, imperative mood description of the change (50 characters or less). This should be capitalized and not end with a period.

4. Provide a more detailed description of the changes if necessary. Wrap each line at 72 characters.

5. If there are any breaking changes, add a description with the prefix "BREAKING CHANGE:".

6. Add a footer with any relevant issue numbers or other references.

Based on this information, please generate a commit message that follows the commitizen format.

## Example:

feat(auth): Implement two-factor authentication

- Add QR code generation for setup
- Implement time-based one-time password (TOTP) validation
- Update user model to store 2FA secret

BREAKING CHANGE: Users will need to set up 2FA on next login

Closes #123

"""

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


def generate_commit_message() -> Iterator[BaseMessage] | None:
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
            ("system", system_template),
            ("user", user_template),
        ]
    )

    model = ChatOpenAI(model=ai_model)
    chain = prompt_template | model

    return chain.stream({"diff": diff})


def print_message(messages: Iterator[BaseMessage]):
    for message in messages:
        print(message.content, end="")


def main():
    check_api_key()

    result = generate_commit_message()

    if result is not None:
        print_message(result)

    print()


if __name__ == '__main__':
    main()
