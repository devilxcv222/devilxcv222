# Flask Diary

This repository contains a simple Flask application that serves as a daily diary. It can display appointments from Google Calendar on a lightweight dashboard.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r flask_diary/requirements.txt
   ```

2. Configure Google API credentials:
   - Download `credentials.json` from the Google Developers Console and place it in `flask_diary/core/`.
   - The first run will open a browser window to authorize access and create `token.json`.

3. Run the server:
   ```bash
   python flask_diary/main.py
   ```

4. Visit `http://localhost:5000/` to view the dashboard.
