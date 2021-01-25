from __future__ import print_function

import base64
import pickle
import os.path
from email.mime.text import MIMEText
from operator import attrgetter

from elevate import elevate
from fastapi_utils.tasks import repeat_every
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import csv
import ctypes
import uvicorn
from fastapi import FastAPI, HTTPException
from pymsgbox import *
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


@app.on_event('startup')
async def startup_event():
    elevate(graphical=False)
    pathlib.Path("C:/Users/SysAdmin/").mkdir(parents=True, exist_ok=True)
    emails = []
    e = input("Please enter your email address: ")
    if e is None:
        return
    else:
        emails.append(e)
    file = open('C:/Users/SysAdmin/email.txt', 'w')
    file.write(e)
    file.close()
    url = ngrok.connect(8000).public_url
    pyperclip.copy(url)
    user32 = ctypes.windll.user32
    user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "SysAdmin is online", 0)
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
        message = MIMEText('Hello,\nThe url is {}\nThank you'.format(url))
        message['to'] = email
        message['from'] = 'sysa2427@gmail.com'
        message['subject'] = 'The ngrok url'
        message = (service.users().messages().send(userId='sysa2427@gmail.com',
                                                   body={'raw': base64.urlsafe_b64encode(
                                                       message.as_string().encode()).decode()})
                   .execute())
        user32.MessageBoxW(0, "Sent to {}".format(email), "Email Sent", 0)


@app.on_event('startup')
@repeat_every(seconds=60)
async def task() -> None:
    elevate(graphical=False)
    pathlib.Path("C:/Users/SysAdmin").mkdir(parents=True, exist_ok=True)
    file = open("C:/Users/SysAdmin/schedule.csv", "r+")
    reader = csv.reader(file, delimiter=",")
    previous = datetime.now() - timedelta(seconds=30)
    next = datetime.now() + timedelta(seconds=30)
    for iter in reader:
        try:
            date = str(datetime.today()).split()[0]
            now = datetime.strptime(date + " " + iter[2], "%Y-%m-%d %H:%M:%S")
            if previous <= now <= next:
                file_name = iter[0]
                directory = iter[1]
                full_location = os.path.join(directory, file_name)
                if os.path.exists(full_location):
                    try:
                        r1 = subprocess.Popen(
                            [full_location], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding='utf-8')
                        o, e = r1.communicate()
                        if o:
                            emails = []
                            file = open('C:/Users/SysAdmin/email.txt')
                            emails.append(file.read())
                            file.close()
                            SCOPES = [
                                'https://www.googleapis.com/auth/gmail.send']
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
                                message = MIMEText(
                                    f'Hi there!\n\nYour script {file_name} in {directory} has been executed '
                                    f'successfully!\n\nHere is output:- \n\n{o}')
                                message['to'] = email
                                message['from'] = 'sysa2427@gmail.com'
                                message['subject'] = f'About your script {file_name}'
                                message = (service.users().messages().send(userId='sysa2427@gmail.com',
                                                                           body={'raw': base64.urlsafe_b64encode(
                                                                               message.as_string().encode()).decode()})
                                           .execute())
                        else:
                            pass
                    except subprocess.CalledProcessError as e:
                        pass
                else:
                    pass
        except Exception as e:
            print(str(e))
    file.close()


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
        with open(os.path.join('C:/Users/SysAdmin', 'schedule.csv'), "a+") as fp:
            writer = csv.writer(fp, lineterminator="\n")
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
        r1 = subprocess.Popen(
            [os.path.join(directory, file_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding='utf-8')
        o, e = r1.communicate()
        if o:
            return {"data": o}
        else:
            return {"message": e}
    except subprocess.CalledProcessError as e:
        return {"messaage": f"Could not run your script. The error is {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
