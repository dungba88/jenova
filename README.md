# jenova

A simple and extensible friendly bot platform written in Python.

## what is Jenova?

Jenova is a bot platform, which can be trained and programmed to do different sort of things. The bot will accept commands as raw plain text (or speech via Speech-to-Text recognition), then translates them into intents, and acts accordingly based on a configured set of code called triggers (see below). An user can extend the bot by train it to recognize new intents, and/or write trigger to handle the intent accordingly. Jenova is intended to run in Lego EV3 robot, but can be installed in PC as well.

jenova consists of 3 main components: `bot`, `server`, and `ui`, all of them are under the folders of the same name.

- **bot**: Receiving raw commands, like `say`, `tell_story`, `inquire.news`. User can write triggers to make it respond to different intents.
- **server**: Translate the text to an intent-based command that the bot can understand using text classification algorithms
- **ui**: A simple interface to the server, can `train`, `talk` and have speech recognition via [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

It can literally **listen** (via Speech-to-Text recognition) and **talk** (via TTS engine), so it almost looks like real bot.

## what is trigger?

Trigger is a piece of code which runs on a specific event. It allows application to be divided into tiny and independence parts. A trigger consists of `event`, `condition` and `action`. Their roles are as below:
- When an `event` occurs (e.g when user says 'good morning')
- If some `condition` holds true (e.g it's actually in the morning)
- Then run some `actions` (e.g response with good morning)

By dividing the application into triggers, the behavior of the bot can be configured, extended and modified easily. For illustration purpose, the jenova project is shipped with 2 separate bot: `sam` and `maruko`. Their configurations (like how to response, the language it speaks and what capabilities it can do) are different.

## what can it do

Well, the bot capabilities depends on what you have trained him to understand, and what intents you have implemented. The current built-in version supports the following types of questions:

- Greetings questions, e.g:

    + Hello/Hi/Good morning/Good afternoon/Good evening
    + What is your name?/How are you?/Who are you?

- Inquire about some general information, e.g:
    
    + What time is it?/What date is it?...
    + What are your hobbies?/What are your interests?...
    + Do you like banana?/Do you like books?...

- Inquire about news, e.g: What is the latest news? What is on trend?
- Inquire about weather: What's the weather like?
- Inquire about entities: What is a galaxy? Where is Andromeda Galaxy?

The questions are obviously not fixed, you can modify it as long as the main keywords are the same. The capabilities of bot will grow as you train him to understand more types of questions.

A demo can be found at: http://jenova.dungba.org/ui/

## running jenova

See this wiki for requirements and installation: [Getting started](https://github.com/dungba88/jenova/wiki/Getting-started)

*to be continued*
