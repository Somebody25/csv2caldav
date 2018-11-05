#!/usr/bin/env python3

import csv
import datetime

def convertdatetime(datetime):
    format = "%Y%m%dT%H%M%SZ";
    return datetime.strftime(format);

events = []

with open("input.csv") as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        event = {}
        date_input = row[0] + ' ' + row[1]
        date_input = datetime.datetime.strptime(date_input, '%d.%m.%Y %H:%M')
        event["datetime"] = convertdatetime(date_input);
        event["summary"] = row[2]
        event["location"] = row[3]
        event["comment"] = row[4]
        events.append(event)

print(events)
