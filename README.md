# ev3

A simple but extensible EV3 bot written in Python and run on ev3dev platform.

## requirements

The following packages need to be installed via `pip`
- **gunicorn**: lightweight WSGI HTTP Server
- **Falcon**: super fast RESTful framework
- **ev3dev**: library for Lego EV3
- **pyttsx**: cross-platform TTS engine
- **mary-tts**: web server for TTS

Python3 is required to run the application

## installation

1. Install the dependencies
```bash
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install gunicorn
sudo pip3 install Falcon
sudo pip3 install ev3dev
sudo pip3 install pyttsx
```

If you want to use `mary-tts` as TTS engine, it must be installed separately:
https://github.com/marytts/marytts/wiki/Local-MaryTTS-Server-Installation

2. Checkout the source code and install the framework
```bash
git clone https://github.com/dungba88/ev3.git
cd ev3
sudo pip3 install framework
```

3. Run the bot
```bash
cd bot #assuming you are in ev3/ folder
gunicorn main -b 0.0.0.0:8080 --reload
```

Now the bot can be accessed from http://localhost:8080. If you install it to your Lego EV3, then change the url to your
Lego EV3 IP address.

*to be continued*
