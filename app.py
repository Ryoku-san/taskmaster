from flask import Flask, render_template, request, redirect, session, url_for
import os
import json
import datetime
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = "taskmaster_secret_key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Remove for production

# Load credentials from environment variable (Render safe)
CLIENT_CONFIG = json.loads(os.environ["GOOGLE_CREDS_JSON"])
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = "https://taskmaster-wweg.onrender.com/oauth2callback"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-task", methods=["POST"])
def add_task():
    title = request.form.get("title")
    time = request.form.get("time")

    session["new_task"] = {"title": title, "time": time}

    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    return redirect("/create_event")

@app.route("/create_event")
def create_event():
    creds_data = session.get("credentials")
    credentials = Credentials(**creds_data)
    service = build("calendar", "v3", credentials=credentials)

    task = session.get("new_task", {})
    start_time = datetime.datetime.fromisoformat(task["time"])
    end_time = start_time + datetime.timedelta(hours=1)

    event = {
        'summary': task["title"],
        'description': 'Task from TaskMaster App',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Africa/Lagos'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Africa/Lagos'},
        'reminders': {'useDefault': True}
    }

    service.events().insert(calendarId='primary', body=event).execute()

    return f"<h3>✅ Task '{task['title']}' added to Google Calendar!</h3><br><a href='/'>← Back to TaskMaster</a>"

def credentials_to_dict(creds):
    return {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
