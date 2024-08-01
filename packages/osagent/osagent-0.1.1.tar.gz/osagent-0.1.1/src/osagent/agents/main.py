import os
import random
import sys
import argparse
import datetime
import logging
import tempfile
import time

from osagent.env.desktop_env import DesktopEnv
from osagent.agents.agent import PromptAgent
from osagent.agents.audio import start_recording, stop_recording, transcribe_audio, text_to_speech_and_play
from pynput import keyboard
import threading


# Start the desktop_env/server/main.py


def on_press(key):
    global recording, stream, filename
    try:
        if key == keyboard.Key.cmd_l or key == keyboard.Key.shift:
            recording.add(keyboard.Key.cmd_l)
            recording.add(keyboard.Key.shift)
        elif key == keyboard.KeyCode(char='x'):
            recording.add(keyboard.KeyCode(char='x'))
            if len(recording) == 3 and stream is None:
                filename = tempfile.mktemp(suffix=".wav")
                stream = start_recording()
    except AttributeError:
        pass


def on_release(key):
    global instruction, stream, filename
    try:
        if key == keyboard.Key.cmd_l or key == keyboard.Key.shift or key == keyboard.KeyCode(char='x'):
            recording.discard(key)
            if len(recording) < 3 and stream is not None:
                stop_recording(stream, filename)
                stream = None
                instruction += transcribe_audio(filename)
                print(instruction)
                filename = None
    except AttributeError:
        pass


# Global variables to track recording state and result
recording = set()
instruction = ""
stream = None

#  Logger Configs {{{ #
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler(
    os.path.join("logs", "normal-{:}.log".format(datetime_str)), encoding="utf-8"
)
debug_handler = logging.FileHandler(
    os.path.join("logs", "debug-{:}.log".format(datetime_str)), encoding="utf-8"
)
stdout_handler = logging.StreamHandler(sys.stdout)
sdebug_handler = logging.FileHandler(
    os.path.join("logs", "sdebug-{:}.log".format(datetime_str)), encoding="utf-8"
)

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.INFO)
sdebug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s"
)
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
sdebug_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("desktopenv"))
sdebug_handler.addFilter(logging.Filter("desktopenv"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)
logger.addHandler(sdebug_handler)
#  }}} Logger Configs #

logger = logging.getLogger("desktopenv.experiment")


def keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark"
    )

    # environment config
    parser.add_argument(
        "--action_space", type=str, default="pyautogui", help="Action type"
    )
    parser.add_argument(
        "--observation_type",
        choices=["screenshot", "a11y_tree", "screenshot_a11y_tree", "som"],
        default="screenshot",
        help="Observation type",
    )
    parser.add_argument("--sleep_after_execution", type=float, default=2)

    # agent config
    parser.add_argument("--max_trajectory_length", type=int, default=3)
    parser.add_argument(
        "--test_config_base_dir", type=str, default="evaluation_examples"
    )

    # lm config
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--platform", type=str, default="macos")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=1500)
    parser.add_argument("--stop_token", type=str, default=None)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    ####### The complete version of the list of examples #######
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    args = config()

    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()

    agent = PromptAgent(
        model=args.model,
        platform=args.platform,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        temperature=args.temperature,
        action_space=args.action_space,
        observation_type=args.observation_type,
        max_trajectory_length=args.max_trajectory_length,

    )

    env = DesktopEnv(
        provider_name="local",
        action_space=agent.action_space,
        require_a11y_tree=args.observation_type in ["a11y_tree", "screenshot_a11y_tree", "som"],
    )

    agent.reset()

    while not instruction:
        text_to_speech_and_play("Hello!!! I'm your personal computer assistant, please give me your instruction.")
        time.sleep(5 + random.randint(0, 10))

    obs = env.reset()

    done = False
    step_idx = 0

    while True:
        response, actions = agent.predict(
            instruction,
            obs
        )

        logger.info("Speech: %s", response.split("```")[0])
        text_to_speech_and_play(response.split("```")[0])

        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)

        step_idx += 1
