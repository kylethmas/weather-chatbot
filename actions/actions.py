import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Text

API_KEY = "cae190d63ed577c1bc29e73afc0768d5"

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

API_KEY = "cae190d63ed577c1bc29e73afc0768d5"

class ActionGetWeather(Action):
    def name(self):
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot("city")
        date = tracker.get_slot("date")
        request_type = tracker.get_slot("request")

        if not city:
            dispatcher.utter_message(text="Please provide a city.")
            return []

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            dispatcher.utter_message(text=f"Sorry, I couldn't find weather data for {city}.")
            return []

        weather_desc = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]

        if request_type == "humidity":
            message = f"The humidity in {city} is {humidity}%."
        elif request_type == "wind":
            message = f"The wind speed in {city} is {wind_speed} m/s."
        else:
            message = f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."

        dispatcher.utter_message(text=message)

        # Reset slots for next conversation
        return [SlotSet("city", None), SlotSet("date", None), SlotSet("request", None)]


class ActionResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("city", None), SlotSet("date", None), SlotSet("request", None)]

class ActionAskMoreDetails(Action):
    def name(self) -> Text:
        return "utter_ask_more_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Do you want to check the humidity, wind, or a different city?")
        return []
