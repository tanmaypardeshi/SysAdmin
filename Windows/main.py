import sys
import ctypes
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

from scripts import services
from scripts import processes
from scripts import ports
from scripts import wmi_template
from scripts import win32_template
from scripts import psutil_template


from pyngrok import ngrok
import pyperclip

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

app = FastAPI()

# Class for service

# class Service(BaseModel):
#     name: str
#     action: Optional[str] = None
#     args: Optional[list] = None

# Class for process

# class Process(BaseModel):
#     pid : int
#     action: Optional[str] = None

# Run as administrator on startup

# @app.on_event('startup')
# def startup_event():
#     url = ngrok.connect(8000).public_url
#     pyperclip.copy(url)
#     user32 = ctypes.windll.user32
#     user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "SysAdmin is online", 0)
# Home route

# @app.get("/")
# def root():
#     return {"Message": "Welome to SysAdmin!"}

# Get all/stopped/running services

# @app.get("/api/services/")
# def get_services(filter: Optional[str] = None, operation : Optional[str] = None):
#     res = services.get_running_services(filter, operation)
#     return res

# Start or stop a particular service

# @app.post("/api/service/")
# def operate_on_service(service : Service):
#     res = services.stop_start_service(service)
#     return res

# Get all processes

# @app.get("/api/processes/")
# def get_processses():
#     res = processes.get_process()
#     return res

# Stop a running process

# @app.post("/api/process/")
# def stop_processes(process : Process):
#     res = processes.stop_or_get_process(process)
#     return res

# Get ports

# @app.get("/api/ports/")
# def get_ports(filter: str):
#     res = ports.get_data(filter)
#     return res

# Class for WMI


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


@app.post("/api/psutil")
def psutil_route(req: Psutil_API):
    res = psutil_template.psutil_controller(req)
    if isinstance(res, str):
        raise HTTPException(400, res)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
