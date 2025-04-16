import json
import logging
import os
import signal
import time
from operator import length_hint

import autoit
from autoit.autoit import Properties as AutoitProps

from Constants import LOG_VIEWER_EXECUTABLE, LOG_VIEWER_DIRECTORY

logger = logging.getLogger(__name__)
SHUTDOWN_DELAY_SECONDS = 10


class Launcher:
    logger = logging.getLogger(__name__)
    log_file_path = None
    log_viewer_pid = None
    programs_file = None

    def __init__(self, programs_file, log_file):
        self.programs_file = programs_file
        self.log_file_path = log_file
        logging.basicConfig(filename=self.log_file_path, filemode='w', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')

        self.log_viewer_pid = autoit.run(filename=f"{LOG_VIEWER_EXECUTABLE} {log_file}",
                                         work_dir=str(LOG_VIEWER_DIRECTORY),
                                         show_flag=AutoitProps.SW_SHOW)

        autoit.win_wait("[TITLE:SnakeTail; CLASS:WindowsForms10.Window.8.app.0.34f5582_r6_ad1]")
        time.sleep(1)

    def execute(self):
        self.logger.info(f"Ready to launch programs from {self.programs_file}")

        with open(self.programs_file) as json_file:
            programs = json.load(json_file)

            for program in programs:
                self.logger.info(f"Launching {program['name']}")

                program_window = program["window"]
                show_flag = action_to_flag(program_window["action"]) if program_window is not None or length_hint(
                    program_window) != 0 else AutoitProps.SW_SHOW

                pid = autoit.run(filename=program["executable"], work_dir=program["work_dir"], show_flag=show_flag)
                time.sleep(5)

                if pid != 0:
                    self.logger.info(f"Started {program["name"]} successfully; PID={pid}")
                else:
                    self.logger.error(f"Failed to start {program["name"]}; Exiting")
                    raise Exception(f"Failed to start {program["name"]}; Exiting")

        self.logger.info(f"Finished. Shutting down in {SHUTDOWN_DELAY_SECONDS} seconds")
        time.sleep(1)
        for i in range(SHUTDOWN_DELAY_SECONDS - 1, 0, -1):
            logger.info(f"{i}")
            time.sleep(1)

        self.logger.info("Closing log viewer now")
        time.sleep(2)

        os.kill(self.log_viewer_pid, signal.SIGTERM)


def action_to_flag(action) -> int:
    result = None
    match action:
        case "show":
            result = AutoitProps.SW_SHOWNORMAL
        case "hide":
            result = AutoitProps.SW_HIDE
        case _:
            logger.error(f"Unknown action {action}\n")
            raise Exception(f"Unknown action {action}\n")
    return result
