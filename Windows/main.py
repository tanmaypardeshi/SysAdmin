from __future__ import print_function

import base64
import pickle
import os.path
from email.mime.text import MIMEText
from operator import attrgetter

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import csv
import ctypes
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import pathlib

from scripts import wmi_template
from scripts import win32_template
from scripts import psutil_template
import subprocess

from pyngrok import ngrok
import pyperclip
import smtplib

# Run as administrator on startup
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

app = FastAPI()


# @app.on_event('startup')
# async def startup_event():
#     url = ngrok.connect(8000).public_url
#     pyperclip.copy(url)
#     user32 = ctypes.windll.user32
#     user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "SysAdmin is online", 0)
#     SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('gmail', 'v1', credentials=creds)
#     for email in ['newalkarpranjal2410.pn@gmail.com', 'kaustubhodak1@gmail.com', 'tanmaypardeshi@gmail.com']:
#         message = MIMEText('Hello,\nThe url is {}\nThank you'.format(url))
#         message['to'] = email
#         message['from'] = 'alumni.vit18@gmail.com'
#         message['subject'] = 'The ngrok url'
#         message = (service.users().messages().send(userId='alumni.vit18@gmail.com',
#                                                    body={'raw': base64.urlsafe_b64encode(
#                                                        message.as_string().encode()).decode()})
#                    .execute())
#         user32.MessageBoxW(0, "Sent to {}".format(email), "Email Sent", 0)


# WMI_API Class
class WMI_API(BaseModel):
    win_class: Optional[str]
    projection: Optional[list]
    match: Optional[dict]
    query: Optional[str]
    func: Optional[str]
    args: Optional[list]


# WMI Endpoint
@app.post("/api/wmi")
def wmi_route(req: WMI_API):
    res = wmi_template.wmi_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return res


# Class for Win32
class Win32_API(BaseModel):
    module: str
    func: str
    args: Optional[list]


# Win32 Endpoint
@app.post("/api/win32")
def win32_route(req: Win32_API):
    res = win32_template.win32_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return res


# Class for psutil
class Psutil_API(BaseModel):
    func: str
    dargs: Optional[dict]


# psutil endpoint
@app.post("/api/psutil")
def psutil_route(req: Psutil_API):
    res = psutil_template.psutil_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return res


class BatScript(BaseModel):
    script: str
    file_name: str
    directory: Optional[str] = 'C:/Users/SysAdmin'
    schedule: Optional[list]
    datetime: Optional[str]


@app.post('/api/create-task')
def bat_route(bat: BatScript):
    file_name, script, directory, schedule = attrgetter(
        'file_name', 'script', 'directory', 'schedule')(bat)
    if file_name.find('.') == -1:
        return {'message': 'Enter file name with correct extension'}
    if isinstance(directory, str):
        if not os.path.exists(directory):
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(directory, file_name), 'w') as batFile:
        batFile.write(script)
    if isinstance(schedule, list):
        with open(os.path.join(directory, 'schedule.csv'), "a+") as fp:
            writer = csv.writer(fp, lineterminator="\n")
            if fp.tell() == 0:
                writer.writerow(["File Name", "Directory", "Time"])
            for s in schedule:
                writer.writerow([file_name, directory, s])
    return {'file_path': os.path.join(directory, file_name)}


class RunScript(BaseModel):
    file_name: str
    directory: Optional[str] = 'C:/Users/SysAdmin/'


@app.post('/api/run-task')
def run_bat(script: RunScript):
    file_name, directory = attrgetter('file_name', 'directory')(script)
    if not os.path.exists(os.path.join(directory, file_name)):
        return {'message': 'File not found, enter correct path'}
    try:
        subprocess.call([os.path.join('C:/Users/SysAdmin', directory, file_name)], shell=True)
    except subprocess.SubprocessError:
        return {'message': 'Could not run your script'}
    return {'success': True}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
