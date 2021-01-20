import wmi
import pythoncom

def get_running_services(filter, operation):
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    arr=[]
    for service in computer.Win32_Service():
        if filter == None:
            arr.append({
                "name":service.Name,
                "description":service.Caption,
                "state": str(service.State).upper(),
                "pathName": service.PathName,
                "startMode": service.StartMode,
                "status": service.Status,
                "systemName": service.SystemName
            })
        elif filter == "running":
            if service.state == 'Running':
                arr.append({
                    "name":service.Name,
                    "description":service.Caption,
                    "state": str(service.State).upper(),
                    "pathName": service.PathName,
                    "startMode": service.StartMode,
                    "status": service.Status,
                    "systemName": service.SystemName
                })
        elif filter == 'stopped':
            if service.state == 'Stopped':
                    arr.append({
                    "name":service.Name,
                    "description":service.Caption,
                    "state": str(service.State).upper(),
                    "pathName": service.PathName,
                    "startMode": service.StartMode,
                    "status": service.Status,
                    "systemName": service.SystemName
                })
    return arr

def stop_start_service(item):
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    try:
        name = item.name
        action = str(item.action).upper()
        w32_svc = computer.Win32_Service(Name=name)[0]
        if action == None:
            return {
                "name": w32_svc.Name,
                "description": w32_svc.Caption,
                "state": str(w32_svc.State).upper(),
                "pathName": w32_svc.PathName,
                "startMode": w32_svc.StartMode,
                "status": w32_svc.Status,
                "systemName": w32_svc.SystemName
            }
        else:
            action = str(action).upper()
            if action == "STOP":
                response = w32_svc.StopService()[0]
                return {"status": f'Stop Service responded with status code: {response} on {name}'}

            elif action == "START":
                response = w32_svc.StartService()[0]
                return {"status": f'Stop Service responded with status code: {response} on {name}'}

    except Exception as e:
        return {"error": str(e)}