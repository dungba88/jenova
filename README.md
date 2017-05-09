# jenova

A simple and extensible friendly bot platform written in Python.

## what is Jenova?

Jenova is a bot platform, which can be trained and programmed to do different sort of things. The bot will accept commands as raw plain text (or speech via Speech-to-Text recognition), then translates them into intents, and acts accordingly based on a configured set of code called triggers (see below). An user can extend the bot by train it to recognize new intents, and/or write trigger to handle the intent accordingly. Jenova is intended to run in Lego EV3 robot, but can be installed in PC as well.

jenova consists of 3 main components: `bot`, `server`, and `ui`, all of them are under the folders of the same name.

- **bot**: Receiving raw commands, like `say`, `tell_story`, `inquire.news`. User can write triggers to make it respond to different intents.
- **server**: Translate the text to an intent-based command that the bot can understand using text classification algorithms
- **ui**: A simple interface to the server, can `train`, `talk` and have speech recognition via [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

It can literally **listen** (via Speech-to-Text recognition) and **talk** (via TTS engine), so it almost looks like real bot.

A demo can be found at: http://jenova.dungba.org/ui/

## what is trigger?

Trigger is a piece of code which runs on a specific event. It allows application to be divided into tiny and independence parts. A trigger consists of `event`, `condition` and `action`. Their roles are as below:
- When an `event` occurs (e.g when user says 'good morning')
- If some `condition` holds true (e.g it's actually in the morning)
- Then run some `actions` (e.g response with good morning)
By dividing the application into triggers, the behavior of the bot can be configured, extended and modified easily. For illustration purpose, the jenova project is shipped with 2 separate bot: `sam` and `maruko`. Their configurations (like how to response, the language it speaks and what capabilities it can do) are different.

## requirements

The following packages need to be installed via `pip`
- `gunicorn`: lightweight WSGI HTTP Server
- `falcon`: super fast RESTful framework
- `httplib2`: HTTP client

For the bot, these packages are required:
- `pygame`: for audio playback
- `pyttsx`, `gTTS`: TTS engines

For the server, these packages are required:
- `sklearn`, `nltk`: for machine learning algorithms and utilities
- `numpy`, `scipy`: libraries used by `sklearn`
- `tinysegmenter`: Japanese tokenizer

Python3 and [ev3dev-lang-python](https://github.com/rhempel/ev3dev-lang-python) are also required to run the application. It's ok to run the application without `ev3dev`, but you won't have the features related to Lego EV3 like motor controlling.

## installation

1. Install the dependencies

It depends on the operating system you are using, here are the example for Ubuntu 17.04

```bash
sudo apt-get install python3 python3-pip python3-ev3dev
sudo pip3 install gunicorn falcon httplib2 pygame pyttsx gTTS numpy scipy sklearn nltk tinysegmenter
```

If you want to use `mary-tts` as TTS engine, it must be installed separately:
https://github.com/marytts/marytts/wiki/Local-MaryTTS-Server-Installation

*(Note that there are some problem with installing and running `pyttsx` with Python3. Checkout [this fork of pyttsx](https://github.com/Julian-O/pyttsx) instead)*

2. Checkout the source code and install the framework
```bash
git clone https://github.com/dungba88/jenova.git
cd jenova
sudo pip3 install framework/
```

3. Run the bot
```bash
gunicorn main --chdir bot/ -b 0.0.0.0:8081 --reload
gunicorn main --chdir server/ -b 0.0.0.0:8080 --reload
```

(You may need to run with `nohup` command)

Now the bot can be accessed from http://localhost:8081 and the server can be accessed from http://localhost:8080

4. Start the UI

For this, you need to install a web server which supports static files, like `Apache` or `nginx`, and make the ui/ folder accessible by HTTP. Setup will depend on which web server you choose.

*to be continued*
