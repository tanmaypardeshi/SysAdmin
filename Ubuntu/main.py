import os
import pickle
import uvicorn
import base64
import pathlib
from email.mime import text
from operator import attrgetter
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


class Script(BaseModel):
    script: str
    file_name: str
    directory: Optional[str] = "/home/SysAdmin/"


@app.on_event('startup')
async def startup_event():
    elevate(graphical=False)
    pathlib.Path("/home/SysAdmin/").mkdir(parents=True, exist_ok=True)
    # emails = []
    # e = prompt(title="Please enter your email address")
    # if e == None:
    #     return
    # else:
    #     emails.append(e)
    # url = ngrok.connect(8000).public_url
    # SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    # creds = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    # service = build('gmail', 'v1', credentials=creds)
    # for email in emails:
    #     message = MIMEText(f'Hello,\nThe URL is {url}\nThank you')
    #     message['to'] = email
    #     message['from'] = 'alumni.vit18@gmail.com'
    #     message['subject'] = 'Your ngrok URL'
    #     message = (service.users().messages().send(userId='alumni.vit18@gmail.com',
    #                                                body={'raw': base64.urlsafe_b64encode(
    #                                                    message.as_string().encode()).decode()})
    #                .execute())
    #     alert(
    #         text=f"The tunneled URL has been sent to {email}", title="Email Sent", button="OK")


@app.get("/")
def root():
    return {"Message": "Welome to SysAdmin!"}


@app.get("/api/services/")
def get_services(filter: Optional[str] = None):
    res = services.get_running_services(filter)
    return res


@app.post("/api/psutil")
def psutil_route(req: PsUtil):
    res = psutil_script.psutil_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return {f"{req.func}": res}


@ app.post("/api/create-task")
def create_task(sc: Script):
    file_name, script, directory = attrgetter(
        'file_name', 'script', 'directory'
    )(sc)
    _, ext = os.path.splitext(file_name)
    if ext == '':
        return {'message': 'Enter file name with correct extension'}
    if isinstance(directory, str):
        if not os.path.exists(directory):
            os.mkdir(directory)
    if directory[-1] == '/':
        with open(f"{directory}{file_name}", 'w') as file:
            file.write(script)
    else:
        with open(f"{directory}/{file_name}", 'w') as file:
            file.write(script)
    return {"message": f"{file_name} writtent to {directory} successfully."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
