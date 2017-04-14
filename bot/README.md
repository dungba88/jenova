# ev3-bot

The implementation for the EV3 bot itself. The bot is a RESTful server, accepting messages and acting 
accordingly via triggers.

Each trigger consists of event, condition and actions. When an event happens, e.g when someone send a 
REST message to the bot server, or when some internal events are raised, if the conditions are matched, then
the robot will execute the corresponding actions. All triggers will run inside a single threaded event loop,
so they won't collide with each other. When an event is raised, the current trigger will stop, and the
triggers corresponding to that event are executed.
