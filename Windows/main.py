import wmi
import sys
import ctypes
import uvicorn
import pythoncom
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

from scripts import services
from scripts import processes
from scripts import ports

from pyngrok import ngrok
import pyperclip
import smtplib

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

app = FastAPI()


# Class for service

class Service(BaseModel):
    name: str
    action: Optional[str] = None
    args: Optional[list] = None


# Class for process

class Process(BaseModel):
    pid: int
    action: Optional[str] = None


# Run as administrator on startup

@app.on_event('startup')
async def startup_event():
    url = ngrok.connect(8000).public_url
    pyperclip.copy(url)
    user32 = ctypes.windll.user32
    user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "SysAdmin is online", 0)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('alumni.vit18@gmail.com', 'Root1234')
        message = 'Subject: The ngrok url\n\nHello,\nThe url is {}\nThank you'.format(url)
        for email in ['newalkarpranjal2410.pn@gmail.com', 'kaustubhodak1@gmail.com', 'tanmaypardeshi@gmail.com']:
            server.sendmail('alumni.vit18@gmail.com', email, message)
            user32.MessageBoxW(0, "Sent to {}".format(email), "Email Sent", 0)
        server.close()


# Home route

@app.get("/")
def root():
    return {"Message": "Welome to SysAdmin!"}


# Get all/stopped/running services

@app.get("/api/services/")
def get_services(filter: Optional[str] = None, operation: Optional[str] = None):
    res = services.get_running_services(filter, operation)
    return res


# Start or stop a particular service

@app.post("/api/service/")
def operate_on_service(service: Service):
    res = services.stop_start_service(service)
    return res


# Get all processes

@app.get("/api/processes/")
def get_processses():
    res = processes.get_process()
    return res


# Stop a running process

@app.post("/api/process/")
def stop_processes(process: Process):
    res = processes.stop_or_get_process(process)
    return res


# Get ports

@app.get("/api/ports/")
def get_ports(filter: str):
    res = ports.get_data(filter)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
