# csv2caldav
This tiny script provides the ability to create calendar events from an csv source.

It connects to a caldav server and adds all the events that are listed in the csv.

## Usage
Clone the repository.

Edit the settings_template.json with the url, username and password used for the caldav and save it as settings.json .

Fill the input.csv with the events that you want to post to the calendar. The csv fields are:

|Date|Time|Topic|Location|Notes|

It will create events with a duration of 1 hour by default.

Then execute the script and the events should appear on your calendar.

## Motivation
I often got a report with many events that I had to manually create on a calendar. This is the automation of this progress, maybe it can help you too.
