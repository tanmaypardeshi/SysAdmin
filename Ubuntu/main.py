from functools import wraps
import os
import csv
import time
import base64
import pickle
import uvicorn
import pathlib
import subprocess
from pymsgbox import *
from pyngrok import ngrok
from email.mime import text
from datetime import datetime, timedelta
from typing import Optional
from elevate import elevate
from pydantic import BaseModel
from operator import attrgetter, ne
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every

from scripts import psutil_script, pysystemd_script

app = FastAPI()


class PsUtil(BaseModel):
    func: str
    dargs: Optional[dict]


class PySystemd(BaseModel):
    class_name: str
    func: str
    dargs: Optional[str]


class Script(BaseModel):
    script: str
    file_name: str
    directory: Optional[str] = "/usr/SysAdmin/"
    datetime: Optional[str]
    schedule: Optional[list]


class RunScript(BaseModel):
    file_name: str
    directory: Optional[str] = "/usr/SysAdmin/"


@ app.on_event('startup')
async def startup_event():
    elevate(graphical=False)
    pathlib.Path("/usr/SysAdmin/").mkdir(parents=True, exist_ok=True)
    emails = []
    file = open('/usr/SysAdmin/email.txt', 'r+')
    emails.append(file.read())
    file.close()
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
        message['from'] = 'sysa2427@gmail.com'
        message['subject'] = 'Your web tunneling URL'
        message = (service.users().messages().send(userId='sysa2427@gmail.com',
                                                   body={'raw': base64.urlsafe_b64encode(
                                                       message.as_string().encode()).decode()})
                   .execute())
        alert(
            text=f"The tunneled URL has been sent to {email}", title="Email Sent", button="OK")


@app.on_event('startup')
@repeat_every(seconds=60)
async def task() -> None:
    elevate(graphical=False)
    pathlib.Path("/usr/SysAdmin/").mkdir(parents=True, exist_ok=True)
    file = open("/usr/SysAdmin/schedule.csv", "r+")
    reader = csv.reader(file, delimiter=",")
    previous = datetime.now() - timedelta(seconds=30)
    next = datetime.now() + timedelta(seconds=30)
    for iter in reader:
        try:
            date = str(datetime.today()).split()[0]
            now = datetime.strptime(date + " " + iter[2], "%Y-%m-%d %H:%M:%S")
            if previous <= now and now <= next:
                file_name = iter[0]
                directory = iter[1]
                full_location = directory + \
                    file_name if directory[-1] == "/" else directory + \
                    "/" + file_name
                if(os.path.exists(full_location)):
                    try:
                        r1 = subprocess.Popen(
                            ['sh', full_location], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                        o, e = r1.communicate()
                        if o:
                            emails = []
                            file = open('/usr/SysAdmin/email.txt')
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
                                    f'Hi there!\n\nYour script {file_name} in {directory} has been executed successfully!\n\nHere is output:- \n\n{o}')
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


@ app.get("/")
def root():
    return {"Message": "Welome to SysAdmin!"}


@ app.post("/api/psutil")
def psutil_route(req: PsUtil):
    res = psutil_script.psutil_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return {f"{req.func}": res}


@ app.post("/api/pysystemd")
def pysystemd_route(req: PySystemd):
    res = pysystemd_script.pysystemd_script(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return {f"{req.class_name}({req.func})": res}


@ app.post("/api/create-task")
def create_task(sc: Script):
    file_name, script, directory, schedule = attrgetter(
        'file_name', 'script', 'directory', 'schedule'
    )(sc)
    _, ext = os.path.splitext(file_name)
    if ext == '':
        return {'message': 'Enter file name with correct extension'}
    if isinstance(directory, str):
        if not os.path.exists(directory):
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    if directory[-1] == '/':
        if os.path.exists(f"{directory}{file_name}"):
            raise HTTPException(
                400, f"{file_name} already exists in {directory}")
        with open(f"{directory}{file_name}", 'w') as file:
            file.write(script)
    else:
        if os.path.exists(f"{directory}/{file_name}"):
            raise HTTPException(
                400, f"{file_name} already exists in {directory}")
        with open(f"{directory}/{file_name}", 'w') as file:
            file.write(script)
    if isinstance(schedule, list):
        with open("/usr/SysAdmin/schedule.csv", "a+") as fp:
            writer = csv.writer(fp, lineterminator="\n")
            for s in schedule:
                writer.writerow([file_name, directory, s])

    return {"message": f"{file_name} written to {directory} successfully."}


@ app.post("/api/run-task")
def run_task(rc: RunScript):
    file_name, directory = attrgetter('file_name', 'directory')(rc)
    full_location = directory + \
        file_name if directory[-1] == "/" else directory + "/" + file_name
    if(os.path.exists(full_location)):
        try:
            r1 = subprocess.Popen(
                ['sh', full_location], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            o, e = r1.communicate()
            if o:
                return {"data": o}
            else:
                return {"message": e}
        except subprocess.CalledProcessError as e:
            return {"messaage": f"Could not run your script. The error is {str(e)}"}
    else:
        return {"message": f"Could not find {file_name} in {directory}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
