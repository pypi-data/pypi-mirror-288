#!/usr/bin/env python3
import requests
import vobject
from datetime import datetime
import json

def main():
    # Assume system time is correct, get current year BornHack phonebook JSON
    url = 'https://bornhack.dk/bornhack-' + str(datetime.now().year) + '/phonebook/json/'   
    json_phonebook = requests.get(url).json()

    for i in json_phonebook['phonebook']:

        j = vobject.vCard()

        # If description is empty, use letters. If both are empty, skip
        text = i['description']
        if text is None:
            text = i['letters']
        if text is None:
            continue

        # Add name
        o = j.add('fn')
        o.value = text

        o = j.add('tel')
        o.param_type = 'cell'
        o.value = i['number']
        
        print(j.serialize())

if __name__ == "__main__":
    main()

