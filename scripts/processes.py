import wmi 
import pythoncom

def get_size(value):
    """
        Scale bytes to its proper format
        e.g: 1253656 => '1.20MB'
    """
    factor = 1024
    l = ["", "K", "M", "G", "T", "P"]
    for unit in range(len(l)):
        if value < factor:
            return f"{value:.2f}{l[unit]}B"
        value /= factor


def get_process():
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    arr = []
    for process in computer.Win32_Process():
        date_time_str = wmi.to_time(process.CreationDate)
        creationTime = str("{:0>2d}".format(int(date_time_str[2])))+"/"+str("{:0>2d}".format(int(date_time_str[1])))+"/"+str(date_time_str[0])+" "+str(
            "{:0>2d}".format(int(date_time_str[3])))+":"+str("{:0>2d}".format(int(date_time_str[4])))+":"+str("{:0>2d}".format(int(date_time_str[5])))
        arr.append({
            "name": str(process.Name),
            "processId": str(process.ProcessId),
            "executablePath": str(process.ExecutablePath),
            "memory": str(get_size(int(process.WorkingSetSize))),
            "creationTime": str(creationTime),
        })
    return arr

def stop_or_get_process(process):
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    pid = process.pid
    action = process.action
    try:
        if action == None:
            response = computer.Win32_Process(PorcessId=pid)
            date_time_str = wmi.to_time(response.CreationDate)
            creationTime = str("{:0>2d}".format(int(date_time_str[2])))+"/"+str("{:0>2d}".format(int(date_time_str[1])))+"/"+str(date_time_str[0])+" "+str(
                "{:0>2d}".format(int(date_time_str[3])))+":"+str("{:0>2d}".format(int(date_time_str[4])))+":"+str("{:0>2d}".format(int(date_time_str[5])))
            return {
                "name": str(process.Name),
                "processId": str(process.ProcessId),
                "executablePath": str(process.ExecutablePath),
                "memory": str(get_size(int(process.WorkingSetSize))),
                "creationTime": str(creationTime),
            }
    except Exception as e:
        return {"error": str(e)}
    else:
        pass
    return None