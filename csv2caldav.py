#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
csv2caldav.py: This script can be used to create calendar events
in a CALDAV calendar from a csv input source
"""

__author__ = "Marcel Körbler"
__copyright__ = "Copyright 2018, Marcel Körbler"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Marcel Körbler"
__email__ = "somebody25@icloud.com"

import csv
import datetime
import uuid
import caldav
import json

payload = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//csv2caldav//EN
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR
"""

def convertdatetime(datetime):
    pattern = "%Y%m%dT%H%M%SZ"
    return datetime.strftime(pattern)

def generateuid():
    return uuid.uuid4()

def main():
    events = []

    with open("settings.json") as settings_file:
        settings = json.load(settings_file)

    with open("input.csv") as file:
        reader = csv.reader(file, delimiter=str(settings['csv'].get('delimiter', ';')))
        for row in reader:
            event = {}
            date_input = row[0] + row[1]
            date_input = datetime.datetime.strptime(date_input, '%d.%m.%Y%H:%M')
            event["uid"] = generateuid()
            event["dtstamp"] = convertdatetime(datetime.datetime.now())
            event["dtstart"] = convertdatetime(date_input)
            event["dtend"] = convertdatetime(date_input + datetime.timedelta(hours=1))
            event["summary"] = row[2]
            event["location"] = row[3]
            event["description"] = row[4]
            events.append(event)

    client = caldav.DAVClient(**settings['connection'])

    calendars = client.principal().calendars()
    for calendar in calendars:
        if calendar.url == settings['connection']['url']:
            for event in events:
                calendar.add_event(payload.format(**event))
                print('Event added!')
            break


if __name__ == '__main__':
    main()
    