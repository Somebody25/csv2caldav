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
import icalendar
import pytz
import io

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

def create_calendar():
    ical = icalendar.Calendar()

    ical.add('version', '2.0')
    ical.add('prodid', '-//csv2caldav//EN')
    return ical

def main():
    events = []

    with open("settings.json") as settings_file:
        settings = json.load(settings_file)

    tz = pytz.timezone('Europe/Vienna')

    with io.open(file="input.csv", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=str(settings['csv'].get('delimiter', ';')))
        for row in reader:
            event = icalendar.Event()
            date_input = row[0] + row[1]
            date_input = datetime.datetime.strptime(date_input, '%d.%m.%Y%H:%M')
            event.add('uid', generateuid())
            event.add('dtstamp', tz.localize(datetime.datetime.now()))
            event.add('dtstart', tz.localize(date_input))
            event.add('dtend', tz.localize(date_input + datetime.timedelta(hours=1)))
            event.add('summary', row[2])
            event.add('location', row[3])
            event.add('description', row[4])
            ical = create_calendar()
            ical.add_component(event)
            events.append(ical)

    client = caldav.DAVClient(**settings['connection'])

    calendars = client.principal().calendars()
    for calendar in calendars:
        if calendar.url == settings['connection']['url']:
            for event in events:
                #print(ical.to_ical())
                calendar.add_event(event.to_ical())


if __name__ == '__main__':
    main()
    