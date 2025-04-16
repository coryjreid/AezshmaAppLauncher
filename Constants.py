import json.encoder
import os
from pathlib import Path

ROOT_DIRECTORY = Path(f"{os.environ.get("APPDATA")}\\Aezshma")
APPLICATION_DIRECTORY = Path(f"{ROOT_DIRECTORY}\\Launcher")

LOG_VIEWER_DIRECTORY = Path(f"{APPLICATION_DIRECTORY}\\bin\\snaketail")
LOG_VIEWER_EXECUTABLE = Path(f"{LOG_VIEWER_DIRECTORY}\\SnakeTail.exe")

DEFAULT_LOG_FILE = Path(f"{APPLICATION_DIRECTORY}\\Launcher.log")

SHUTDOWN_DELAY_SECONDS = 10
