import wmi
import pythoncom

Win32_Service_Keys = [
    'AcceptPause',
    'AcceptStop',
    'Caption',
    'CheckPoint',
    'CreationClassName',
    'DelayedAutoStart',
    'Description',
    'DesktopInteract',
    'DisplayName',
    'ErrorControl',
    'ExitCode',
    'InstallDate',
    'Name',
    'PathName',
    'ProcessId',
    'ServiceSpecificExitCode',
    'ServiceType',
    'Started',
    'StartMode',
    'StartName',
    'State',
    'Status',
    'SystemCreationClassName',
    'SystemName',
    'TagId',
    'WaitHint'
]

Win32_Service_Actions = [
    'StartService',
    'StopService',
    'PauseService',
    'ResumeService',
    'InterrogateService',
    'UserControlService',
    'Create',
    'Change',
    'ChangeStartMode',
    'Delete',
    'GetSecurityDescriptor',
    'SetSecurityDescriptor'
]


def get_running_services(filter, operation):
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    arr = []
    service_args = {}
    properties = ["Caption", "State", "ProcessId"]
    if filter != None:
        service_args = {"State": filter}

    for service in computer.Win32_Service(properties, **service_args):
        svc_obj = {}
        for k in ["Name"] + properties:
            svc_obj[k] = getattr(service, k)
        arr.append(svc_obj)
    return arr


def stop_start_service(item):
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    try:
        name = item.name
        action = item.action
        args = []
        w32_svc = computer.Win32_Service(Name=name)[0]
        if action == None:
            obj = {}
            for k in Win32_Service_Keys:
                obj[k] = getattr(w32_svc, k)
            return obj
        else:
            if action not in Win32_Service_Actions:
                raise Exception('Invalid Action provided')
            if item.args and isinstance(item.args, list):
                args = item.args
            response = getattr(w32_svc, action)(*args)[0]
            return {"status": f'{action} responded with status code: {response} on {name}'}
    except Exception as e:
        return {"error": str(e)}
