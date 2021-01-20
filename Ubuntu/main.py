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


app = FastAPI()

# Class for service

class Service(BaseModel):
    name: str
    action: Optional[str] = None

# Class for process

class Process(BaseModel):
    pid : int
    action: Optional[str] = None

# Run as administrator on startup

@app.on_event('startup')
async def startup_event():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Home route

@app.get("/")
def root():
    return {"Message": "Welome to SysAdmin!"}

# Get all/stopped/running services

@app.get("/api/services/")
def get_services(filter: Optional[str] = None, operation : Optional[str] = None):
    res = services.get_running_services(filter, operation)
    return res

# Start or stop a particular service

@app.post("/api/service/")
def operate_on_service(service : Service):
    res = services.stop_start_service(service)
    return res

# Get all processes

@app.get("/api/processes/")
def get_processses():
    res = processes.get_process()
    return res

# Stop a running process

@app.post("/api/process/")
def stop_processes(process : Process):
    res = processes.stop_or_get_process(process)
    return res

# Get ports

@app.get("/api/ports/")
def get_ports(filter: str):
    res = ports.get_data(filter)
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)