# OSAgent

OSAgent is a demo application designed to assist users through voice commands on their computers. It supports Ubuntu, Windows, and macOS systems, can run in the background, and integrates voice input. The application leverages advanced models based on the [OSWorld](https://os-world.github.io/) benchmark for quick integration and efficient functionality.

## Features

- **Cross-Platform**: Works on Ubuntu, Windows, and macOS.
- **Background Operation**: Continuously runs without disrupting other tasks.
- **Voice Input**: Accepts and processes voice commands.
- **Advanced Model Integration**: Utilizes OSWorld benchmark models for enhanced performance.

## Installation and Running

To get started with OSAgent, follow these steps:

1. Set your OpenAI API key:
   ```shell
   export OPENAI_API_KEY="YOUR_KEY"
   ```

2. Install the OSAgent package:
   ```shell
   pip install osagent
   ```

3. Run the main agent module:
   ```shell
   python -m osagent.agents.main
   ```

**Note:** On macOS, you may receive popups requesting network, screenshot, or accessibility permissions. Please grant these permissions for OSAgent to function correctly.

## Usage

In default the program run in voice command feature, please press and hold the combination of `shift + ctrl + x`, then speak your instruction and release the keys to process the command.

For more detailed information, please refer to our [documentation](https://os-world.github.io/).

