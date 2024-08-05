from pathlib import Path

import PyInstaller.__main__

CURRENT_SCRIPT_PATH = Path(__file__).parent
MAIN_FILE = CURRENT_SCRIPT_PATH / "src" / "ai_commit" / "ai_commit.py"
APP_NAME = "ai-commit"


def build():
    PyInstaller.__main__.run([
        str(MAIN_FILE),
        "--onefile",
        "--name",
        APP_NAME,
        "--console",
    ])


if __name__ == '__main__':
    build()
