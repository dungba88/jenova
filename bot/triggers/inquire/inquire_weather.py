"""Trigger implementation for inquiring weather"""

from utils import tts
from utils import dynamic_facts

class InquireWeather(object):
    """Trigger to inquire weather"""

    def run(self, execution_context, app_context):
        """run the action"""
        opening_reacts = app_context.get_config('behavior.weather_react.opening')
        tts.say_random(opening_reacts)

        # get weather info
        weather = dynamic_facts.get_weather()
        main_weather = weather['weather'][0]['main']
        clouds = weather['clouds']['all']
        temp = weather['main']['temp'] - 273 # convert from Kelvin
        pressure = weather['main']['pressure']
        humidity = weather['main']['humidity']

        react_config = app_context.get_config('behavior.weather_react')

        main_weather_react = react_config.get('main.' + main_weather, [])
        clouds_react = react_config.get('clouds', [])
        temp_react = react_config.get('temp', [])
        pressure_react = react_config.get('pressure', [])
        humidity_react = react_config.get('humidity', [])

        tts.say_random_finish(main_weather_react, execution_context)
        tts.say_random(clouds_react, {'clouds' : clouds})
        tts.say_random(temp_react, {'temp' : int(temp)})
        tts.say_random(pressure_react, {'pressure' : pressure})
        tts.say_random(humidity_react, {'humidity' : humidity})
