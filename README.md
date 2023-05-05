# HushVC

## Description
This project is a Discord bot that handles live voice interactions and passes them to a series of AI models using base [Pycord](https://github.com/Pycord-Development/pycord) and some custom class implementations.
**This is still very much in early development as getting live-streamed audio data from discord has proven to be somewhat difficult.**
As such, many features are still to-be-developed.

## Features
- Connects to Discord voice channels
- Streams live audio data from voice channels to a responsive AI
- Configurable settings for AI model selection and audio data preprocessing

## Installation
1. Clone this repository: `git clone https://github.com/ScruffyTheMoose/HushVC.git`
2. Install dependencies: `pip install requirements.txt`
4. Start the bot: `python app/bot.py`

## Usage
1. Invite the bot to your Discord server.
2. Join a voice channel and type `!join` to make the bot join the same channel.
3. The bot will stream audio data from the voice channel to the underlying model and respond (hopefully quickly) back over voice.
4. End the interaction with the `!leave` command.

## Configuration
Custom configuration of the bot is still to-be-developed.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See `LICENSE` for more information.
