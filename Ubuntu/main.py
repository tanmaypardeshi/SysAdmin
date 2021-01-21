import uvicorn
from elevate import elevate
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

from scripts import services, psutil_script

app = FastAPI()

# Class for service


class Service(BaseModel):
    name: str
    action: Optional[str] = None

# Class for process


class Process(BaseModel):
    pid: int
    action: Optional[str] = None


class PsUtil(BaseModel):
    func: str
    dargs: Optional[dict]

    # Run as administrator on startup


@app.on_event('startup')
async def startup_event():
    elevate(graphical=False)

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
