# ev3

A simple but extensible EV3 bot written in Python and run on ev3dev platform.

## requirements

The following packages need to be installed via `pip`
- `gunicorn`: lightweight WSGI HTTP Server
- `Falcon`: super fast RESTful framework

For the bot, these packages are required:
- `pygame`: for audio playback
- `pyttsx`, `gTTS`: TTS engines

For the server, these packages are required:
- `sklearn`, `nltk`: for machine learning algorithms and utilities
- `numpy`, `scipy`: libraries used by `sklearn`

Python3 and [ev3dev-lang-python](https://github.com/rhempel/ev3dev-lang-python) are also required to run the application. It's ok to run the application without `ev3dev`, but you won't have the features related to Lego EV3 like motor controlling.

## installation

1. Install the dependencies

It depends on the operating system you are using, here are the example for Ubuntu 17.04

```bash
sudo apt-get install python3 python3-pip python3-ev3dev
sudo pip3 install gunicorn Falcon pygame pyttsx gTTS numpy scipy sklearn nltk
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
cd bot # assuming you are in ev3/ folder
gunicorn main -b 0.0.0.0:8081 --reload
```

4. Run the server
```bash
cd ../server # assuming you are in bot/ folder
gunicorn main -b 0.0.0.0:8080 --reload

Now the bot can be accessed from http://localhost:8081 and the server can be accessed from http://localhost:8080

5. Start the UI

For this, you need to install a web server which supports static files, like `Apache` or `nginx`, and make the ui/ folder accessible by HTTP. Setup will depend on which web server you choose.

*to be continued*
