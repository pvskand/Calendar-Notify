from __future__ import print_function
import httplib2
import os
import subprocess
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
 
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    dateNow = datetime.datetime.now().date()
    
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    reminder = [False for i in range(1,5+1)]
    print(len(events))
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date = str(event['start'].get('dateTime'))
        dateToday = str(date[0:10])
        startTime = str(date[11:19])
        string_date = dateToday + " "+startTime + ".0"
        string_date_oneHour = dateToday + " 01:00:00.0"
        startTimeDate = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")
        oneHour = datetime.datetime.strptime(string_date_oneHour, "%Y-%m-%d %H:%M:%S.%f")
        print(startTimeDate - datetime.datetime.now(), "hello")
        if(datetime.datetime.now() < startTimeDate):
        	timeLeft = startTimeDate - datetime.datetime.now()
        	timeLeft = "in "+ str(timeLeft) + " hrs"
        	subprocess.Popen(['notify-send', event['summary'], timeLeft])

        print(start, event['summary'])


if __name__ == '__main__':
    main()
