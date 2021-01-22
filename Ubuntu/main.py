from email.mime import text
import pickle
import uvicorn
import os.path
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pyngrok import ngrok
from elevate import elevate
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from pymsgbox import *

from scripts import services, psutil_script

app = FastAPI()


class PsUtil(BaseModel):
    func: str
    dargs: Optional[dict]


@app.on_event('startup')
async def startup_event():
    elevate(graphical=False)
    emails = []
    e = prompt(title="Please enter your email address")
    if e == None:
        return
    else:
        emails.append(e)
    url = ngrok.connect(8000).public_url
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    for email in emails:
        message = MIMEText(f'Hello,\nThe URL is {url}\nThank you')
        message['to'] = email
        message['from'] = 'alumni.vit18@gmail.com'
        message['subject'] = 'Your ngrok URL'
        message = (service.users().messages().send(userId='alumni.vit18@gmail.com',
                                                   body={'raw': base64.urlsafe_b64encode(
                                                       message.as_string().encode()).decode()})
                   .execute())
        alert(
            text=f"The tunneled URL has been sent to {email}", title="Email Sent", button="OK")

# Home route


@app.get("/")
def root():
    return {"Message": "Welome to SysAdmin!"}

# Get all/stopped/running services


@app.get("/api/services/")
def get_services(filter: Optional[str] = None):
    res = services.get_running_services(filter)
    return res


# psutil implmentation

@app.post("/api/psutil")
def psutil_route(req: PsUtil):
    res = psutil_script.psutil_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
