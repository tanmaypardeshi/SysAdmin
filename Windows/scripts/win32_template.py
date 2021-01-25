import win32._winxptheme
import win32.mmapfile
import win32.odbc
import win32.perfmon
import win32.servicemanager
import win32.timer
import win32.win32ras
import win32.win2kras
import win32.win32api
import win32.win32clipboard
import win32.win32console
import win32.win32cred
import win32.win32crypt
import win32.win32event
import win32.win32evtlog
import win32.win32file
import win32.win32gui
import win32.win32help
import win32.win32inet
import win32.win32job
import win32.win32lz
import win32.win32net
import win32.win32pdh
import win32.win32pipe
import win32.win32print
import win32.win32process
import win32.win32profile
import win32.win32security
import win32.win32service
import win32.win32transaction
import win32.win32ts
import win32.win32wnet
from operator import attrgetter
# module = 'win32api'
# fn = 'Beep'
# args = [250, 1000]

# getattr(getattr(win32, module), fn)(*args)


def win32_controller(req):
    try:
        module, func, args = attrgetter('module', 'func', 'args')(req)
        args = args if isinstance(args, list) else []
        return getattr(getattr(win32, module), func)(*args)
    except Exception as e:
        return str(e)
