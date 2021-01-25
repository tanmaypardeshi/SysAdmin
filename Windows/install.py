import subprocess
from os import path
import ctypes, sys

def getabspath(filename: str) -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
        return path.abspath(path.join(bundle_dir, filename))
    
    return path.abspath(path.join(path.dirname(__file__), filename))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    email = input('Enter your email: ')
    nssmpath = getabspath('nssm.exe')
    exepath = getabspath('SAC.exe')
    subprocess.run(args=[nssmpath, 'install', 'SAC', exepath, email], shell=True)
    subprocess.run(args=[nssmpath, 'set', 'SAC', 'Description', 'SysAdmin Client Application'], shell=True)
    subprocess.run(args=[nssmpath, 'set', 'SAC', 'AppDirectory', getabspath('')], shell=True)
    subprocess.run(args=[nssmpath, 'start', 'SAC'])
    input('Press Enter to continue...')
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)