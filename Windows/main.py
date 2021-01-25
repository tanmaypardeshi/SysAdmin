from __future__ import print_function
from threading import Thread

import base64
import pickle
from os import path, environ, getenv
from email.mime.text import MIMEText
from operator import attrgetter

from elevate import elevate
from fastapi_utils.tasks import repeat_every
from datetime import date, datetime, timedelta
import smtplib
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

from dotenv import load_dotenv
load_dotenv()

# Run as administrator on startup
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

def getabspath(filename):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = getattr(
            sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
        return path.abspath(path.join(bundle_dir, filename))

    return path.abspath(path.join(path.dirname(__file__), filename))

if getenv('EMAIL') is None and len(sys.argv) == 1:
    sys.exit('Email not supplied, exiting')
else:
    environ['EMAIL'] = sys.argv[1] if len(sys.argv) == 2 else getenv('EMAIL')
    with open(getabspath('.env'), 'w') as env_file:
        env_file.write("EMAIL=" + environ['EMAIL'])

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    pathlib.Path("C:/Users/SysAdmin/").mkdir(parents=True, exist_ok=True)
    url = ngrok.connect(8000).public_url
    pyperclip.copy(url)
    user32 = ctypes.windll.user32
    # Thread(target=lambda: user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "SysAdmin is online", 0)).start()
    msgBox = "URI: " + url + " copied to clipboard"
    email = getenv('EMAIL')
    if email is not None:
        msgBox = msgBox + ", and sent to " + email + "."
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('sysa2427@gmail.com', 'SysAdmin2427')
            message = 'Subject: SysAdminClient is active\n\nSysAdminClient is running on ' + url
            server.sendmail(
                'sysa2427@gmail.com',
                email,
                message
            )

    Thread(target=lambda: user32.MessageBoxW(0, msgBox, "SysAdmin is online", 0)).start()


@app.on_event('startup')
@repeat_every(seconds=60)
async def task() -> None:
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
                full_location = path.join(directory, file_name)
                if path.exists(full_location):
                    try:
                        r1 = subprocess.Popen(
                            [full_location], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding='utf-8')
                        o, e = r1.communicate()
                        if o:
                            email = getenv('EMAIL')
                            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                                server.login('sysa2427@gmail.com', 'SysAdmin2427')
                                message = f'Subject: About your script {file_name}\n\nHi there!\n\nYour script {file_name} in {directory} has been executed successfully!\n\nHere is output:- \n\n{o}'
                                server.sendmail(
                                    'sysa2427@gmail.com',
                                    email,
                                    message
                                )
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
        if not path.exists(directory):
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    with open(path.join(directory, file_name), 'w') as batFile:
        batFile.write(script)
    if isinstance(schedule, list):
        with open(path.join('C:/Users/SysAdmin', 'schedule.csv'), "a+") as fp:
            writer = csv.writer(fp, lineterminator="\n")
            for s in schedule:
                writer.writerow([file_name, directory, s])
    return {'file_path': path.join(directory, file_name)}


class RunScript(BaseModel):
    file_name: str
    directory: Optional[str] = 'C:/Users/SysAdmin/'


@app.post('/api/run-task')
def run_bat(script: RunScript):
    file_name, directory = attrgetter('file_name', 'directory')(script)
    if not path.exists(path.join(directory, file_name)):
        return {'message': 'File not found, enter correct path'}
    try:
        r1 = subprocess.Popen(
            [path.join(directory, file_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding='utf-8')
        o, e = r1.communicate()
        if o:
            return {"data": o}
        else:
            return {"message": e}
    except subprocess.CalledProcessError as e:
        return {"messaage": f"Could not run your script. The error is {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
