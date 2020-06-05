import requests
import json
import pyttsx3
import speech_recognition as sr
import re


class Data:
    def __init__(self):
        self.data = self.get_data()

    def get_data(self):
        response = requests.get("https://covid19indapi.herokuapp.com/india")
        data = response.json()
        return data

    def get_state_data(self, state):
        data = self.data['state']

        for content in data:
            if content['state_name'].lower() == state.lower():
                return content

    def get_list_of_states(self):
        states = []
        for state in self.data['state']:
            states.append(state['state_name'].lower())
        return states


data = Data()

print(data.get_list_of_states())


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


def main():
    print("Started Program")
    data = Data()
    END_PHRASE = "stop"
    state_list = data.get_list_of_states()

    STATE_PATTERN = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda state_list: data.get_state_data(state_list)['confirmed'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda state_list: data.get_state_data(state_list)['deaths'],
    }

    while True:
        print('Listning..')
        text = get_audio()
        print(text)
        result = None

        for pattern, func in STATE_PATTERN.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for state in state_list:
                    if state in words:
                        result = func(state)
                        break

        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:
            print("ended")
            break


main()
