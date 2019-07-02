#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
csv2caldav.py: This script can be used to create calendar events
in a CALDAV calendar from a csv input source
"""

__author__ = "Marcel Körbler"
__copyright__ = "Copyright 2018, Marcel Körbler"
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Marcel Körbler"
__email__ = "somebody25@icloud.com"

import csv
import datetime
import uuid
import caldav
import json
import icalendar
import pytz
import click
import os

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

@click.command()
@click.option('-t', '--timezone', type=str, default='Europe/Vienna', help='Specify the timezone when the events take place. Default: Europe/Vienna')
@click.option('-d', '--delimiter', type=str, default=';', help='The delimiter used in the input csv. Default: ;')
@click.option('-s', '--settings-file', type=click.File('r'), default=os.path.realpath("./settings.json"), help='Set the settings file')
@click.option('--time-delta', type=int, default=60, help='The duration of the events in minutes. Default: 60')
@click.option('--print-ical', is_flag=True, help='Print the generated icalendar request')
@click.argument('input-file', type=click.File(mode='r', encoding='UTF-8'))
def main(timezone, delimiter, settings_file, time_delta, print_ical, input_file):
    click.echo('csv2caldav v' + __version__)

    events = []

    click.echo('Loading settings')
    settings = json.load(settings_file)

    click.echo('Using timezone: ' + timezone)
    tz = pytz.timezone(timezone)

    click.echo('Parsing csv')
    reader = csv.reader(input_file, delimiter=delimiter)
    for row in reader:
        event = icalendar.Event()
        date_input = row[0] + row[1]
        date_input = datetime.datetime.strptime(date_input, '%d.%m.%Y%H:%M')
        event.add('uid', generateuid())
        event.add('dtstamp', tz.localize(datetime.datetime.now()))
        event.add('dtstart', tz.localize(date_input))
        event.add('dtend', tz.localize(date_input + datetime.timedelta(minutes=time_delta)))
        event.add('summary', row[2])
        event.add('location', row[3])
        event.add('description', row[4])
        ical = create_calendar()
        ical.add_component(event)
        events.append(ical)

    click.echo('Found events: ' + str(len(events)))

    client = caldav.DAVClient(**settings['connection'])

    if print_ical:
        for event in events:
            click.echo(event.to_ical())

    if click.confirm('Send to calendar?'):
        calendars = client.principal().calendars()
        for calendar in calendars:
            if calendar.url == settings['connection']['url']:
                for event in events:
                    calendar.add_event(event.to_ical())
                    click.echo('--Added event!--')


if __name__ == '__main__':
    main()
    