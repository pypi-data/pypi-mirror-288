import os
import subprocess
import signal
import logging
import threading

from osagent.env.providers.base import Provider

logger = logging.getLogger("desktopenv.providers.local.LocalProvider")
logger.setLevel(logging.INFO)


class LocalProvider(Provider):
    def __init__(self, region: str = None, conda_env: str = "base"):
        super().__init__(region)
        self.process = None
        self.conda_env = conda_env

    def start_emulator(self, path_to_vm: str, headless: bool):
        def run():
            logger.info("Starting OSWorld service locally...")

            # Prepare the command to run the emulator
            # Get the absolute path to the directory of this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_script_path = os.path.abspath(os.path.join(current_dir, '../../server/main.py'))

            command = ['python', main_script_path]

            # Run the command directly
            subprocess.run(command, shell=False)

            logger.info("OSWorld service started")

        # Create a new thread to run the emulator
        self.process_thread = threading.Thread(target=run)
        self.process_thread.start()
        logger.info("OSWorld service started in a new thread")

    def get_ip_address(self, path_to_vm: str) -> str:
        return "localhost"

    def save_state(self, path_to_vm: str, snapshot_name: str):
        pass

    def revert_to_snapshot(self, path_to_vm: str, snapshot_name: str):
        pass

    def stop_emulator(self, path_to_vm, region=None):
        logger.info("Stopping OSWorld service locally...")

        # If the process was started, terminate it
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.wait()

            logger.info("OSWorld service with PID %s has been stopped", self.process.pid)
            self.process = None
        else:
            logger.warning("OSWorld service is not running")