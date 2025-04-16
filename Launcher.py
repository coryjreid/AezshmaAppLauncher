import json
import logging
import os
import signal
import time
from operator import length_hint
from xml.etree import ElementTree

import autoit
from autoit.autoit import Properties as AutoitProps

from Constants import LOG_VIEWER_EXECUTABLE, LOG_VIEWER_SESSION_FILE

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

        edit_xml(LOG_VIEWER_SESSION_FILE, "FilePath", f"{log_file}")
        self.log_viewer_pid = autoit.run(filename=f"{LOG_VIEWER_EXECUTABLE} {LOG_VIEWER_SESSION_FILE}")

        autoit.win_wait("[TITLE:SnakeTail; CLASS:WindowsForms10.Window.8.app.0.34f5582_r6_ad1]")
        time.sleep(1)

    def execute(self):
        self.logger.info(f"Ready to launch programs from {self.programs_file}")

        with open(self.programs_file) as json_file:
            programs = json.load(json_file)
            self.logger.info(f"Programs file loaded successfully")

            self.logger.info(f"Launching {len(programs)} programs")
            count = 1
            for program in programs:
                self.logger.info(f"({count}/{len(programs)}) Starting {program['name']}")

                pid = autoit.run(filename=program["executable"], work_dir=program["work_dir"])

                if pid != 0:
                    self.logger.info(f"Started {program["name"]} successfully; PID={pid}")
                    count += 1

                    program_window = program["window"]
                    if program_window is not None or length_hint(program_window) == 2:
                        self.logger.info(f"Waiting for {program["name"]} window")

                        show_flag = action_to_flag(program_window["action"])
                        autoit.win_wait(program_window["title"])  # wait for window to exist
                        time.sleep(1)
                        handle = autoit.win_get_handle(program_window["title"])
                        autoit.win_set_state_by_handle(handle, show_flag)

                        self.logger.info(f"Set {program["name"]} window state successfully")
                        time.sleep(1)

                else:
                    self.logger.error(f"Failed to start {program["name"]}; Exiting")
                    exit(1)

        self.logger.info(f"Finished. Shutting down in {SHUTDOWN_DELAY_SECONDS} seconds")
        time.sleep(1)
        for i in range(SHUTDOWN_DELAY_SECONDS - 1, 0, -1):
            logger.info(f"{i}")
            time.sleep(1)

        self.logger.info("Closing log viewer now")
        time.sleep(2)

        os.kill(self.log_viewer_pid, signal.SIGTERM)


def action_to_flag(action) -> int:
    match action:
        case "show":
            result = AutoitProps.SW_SHOWNORMAL
        case "hide":
            result = AutoitProps.SW_HIDE
        case "minimize":
            result = AutoitProps.SW_MINIMIZE
        case "maximize":
            result = AutoitProps.SW_MAXIMIZE
        case "restore":
            result = AutoitProps.SW_RESTORE
        case _:
            logger.error(f"Unsupported action {action}; Exiting")
            exit(1)
    return result


def edit_xml(xml_file, element_tag, new_text=None, attribute_name=None, attribute_value=None):
    """
    Edits an XML file.

    Args:
        xml_file (str): Path to the XML file.
        element_tag (str): Tag name of the element to edit.
        new_text (str, optional): New text for the element. Defaults to None.
        attribute_name (str, optional): Name of the attribute to edit. Defaults to None.
        attribute_value (str, optional): New value for the attribute. Defaults to None.
    """
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

    for element in root.iter(element_tag):
        if new_text is not None:
            element.text = new_text
        if attribute_name is not None and attribute_value is not None:
            element.set(attribute_name, attribute_value)

    tree.write(xml_file)
