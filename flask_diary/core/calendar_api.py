"""Google Calendar integration module."""

from __future__ import annotations

import os
from datetime import datetime
from typing import List, Dict

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Scope for reading calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')


def _get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(day: datetime) -> List[Dict[str, str]]:
    """Return a list of events for a specific day."""
    try:
        service = _get_service()
    except Exception:
        # Google API not configured
        return []

    start = datetime.combine(day, datetime.min.time()).isoformat() + 'Z'
    end = datetime.combine(day, datetime.max.time()).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = []
    for item in events_result.get('items', []):
        start_time = item['start'].get('dateTime', item['start'].get('date'))
        summary = item.get('summary', 'No Title')
        events.append({'start': start_time, 'summary': summary})
    return events
