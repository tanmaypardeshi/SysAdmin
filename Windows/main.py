import sys
import ctypes
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

from scripts import wmi_template
from scripts import win32_template
from scripts import psutil_template


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
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#         server.login('alumni.vit18@gmail.com', 'Root1234')
#         message = 'Subject: The ngrok url\n\nHello,\nThe url is {}\nThank you'.format(url)
#         for email in ['newalkarpranjal2410.pn@gmail.com', 'kaustubhodak1@gmail.com', 'tanmaypardeshi@gmail.com']:
#             server.sendmail('alumni.vit18@gmail.com', email, message)
#             user32.MessageBoxW(0, "Sent to {}".format(email), "Email Sent", 0)
#         server.close()


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
