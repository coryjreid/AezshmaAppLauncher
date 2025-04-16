import argparse
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

from Constants import ROOT_DIRECTORY, APPLICATION_DIRECTORY, LOG_VIEWER_DIRECTORY, DEFAULT_LOG_FILE
from Launcher import Launcher

parser = argparse.ArgumentParser(prog="LauncherMain", description="Launches a number of processes in sequence")
parser.add_argument("-p", "--programs_file", help="The JSON file defining the programs to launch", required=True)
parser.add_argument("-l", "--log_file", help="The file this application logs to", required=False)
args = parser.parse_args()

log_file = args.log_file
programs_file = args.programs_file


def main() -> None:
    setup()
    Launcher(programs_file, log_file).execute()


def setup() -> None:
    global log_file, programs_file

    if not Path(programs_file).is_file():
        print(f"Program file {programs_file} does not exist")
        exit(1)
    else:
        programs_file = Path(programs_file)

    if not ROOT_DIRECTORY.exists():
        ROOT_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)

    if not APPLICATION_DIRECTORY.exists():
        APPLICATION_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)

    if not LOG_VIEWER_DIRECTORY.exists():
        LOG_VIEWER_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)
        http_response = urlopen(
            "https://github.com/snakefoot/snaketail-net/releases/download/1.9.8/SnakeTail_v1.9.8.zip")
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(path=LOG_VIEWER_DIRECTORY)

    log_file = Path(log_file) if log_file is not None else DEFAULT_LOG_FILE
    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w") as f:
            f.write("")


if __name__ == "__main__":
    main()
