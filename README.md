# ev3

A simple but extensible EV3 bot written in Python and run on ev3dev platform.

## requirements

The following packages need to be installed via `pip`
- **gunicorn**: lightweight WSGI HTTP Server
- **Falcon**: super fast RESTful framework
- **pygame**: for audio playback
- **pyttsx**: cross-platform TTS engine
- **gTTS**: wrapper for Google Translate TTS

Python3 and [ev3dev-lang-python](https://github.com/rhempel/ev3dev-lang-python) are also required to run the application

## installation

1. Install the dependencies

It depends on the operating system you are using, here are the example for Ubuntu 17.04

```bash
sudo apt-get install python3 python3-pip python3-ev3dev
sudo pip3 install gunicorn Falcon pygame pyttsx gTTS ev3dev
```

If you want to use `mary-tts` as TTS engine, it must be installed separately:
https://github.com/marytts/marytts/wiki/Local-MaryTTS-Server-Installation

*(Note that there are some problem with installing and running `pyttsx` with Python3. Checkout [this fork of pyttsx](https://github.com/Julian-O/pyttsx) instead)*

2. Checkout the source code and install the framework
```bash
git clone https://github.com/dungba88/ev3.git
cd ev3
sudo pip3 install framework/
```

3. Run the bot
```bash
cd bot #assuming you are in ev3/ folder
gunicorn main -b 0.0.0.0:8080 --reload
```

Now the bot can be accessed from http://localhost:8080. If you install it to your Lego EV3, then change the url to your
Lego EV3 IP address.

4. Optionally configure the engine and voice

Take a look at the file `bot/configs/engine.json`. Currently the following TTS engine are supported:
- `pyttsx`: cross-platform
- `osx`: only for MacOS via `say` command
- `gTTS`: wrapper for Google Translate TTS. very limited support
- `ev3dev`: wrapper for `espeak` in Linux. does not support voice change, but you can modify it to change the voice
- `mary-tts`: client for MaryTTS. can support a wide range of voices. it supports caching of audio files for faster performance

*to be continued*
