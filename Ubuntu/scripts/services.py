import subprocess


def format_description(line):
    line = line.split()[4:]
    return (',').join(line).replace(',', ' ')


def get_running_services(filter):
    result = None
    if type(filter) == 'str':
        filter = filter.lower()
    if filter == 'running':
        result = subprocess.check_output(
            'sudo systemctl list-units --type=service --state=active | grep -v not-found', shell=True, universal_newlines=True, encoding='utf-8')
    elif filter == 'stopped':
        result = subprocess.check_output(
            'sudo systemctl list-units --type=service --state=inactive | grep -v not-found', shell=True, universal_newlines=True, encoding='utf-8')
    else:
        result = subprocess.check_output(
            'sudo systemctl list-units --type=service --state=active,inactive | grep -v not-found', shell=True, universal_newlines=True, encoding='utf-8')
    iterator = iter(result.splitlines())
    next(iterator)

    services = []
    for line in iterator:
        try:
            obj = {}
            name = line.split()[0]
            status = ""
            description = ""
            if line.split()[2] == 'active':
                status = "RUNNING"
            else:
                status = "STOPPED"
            description = format_description(line)
            obj = {"name": name, "description": description, "status": status}
            services.append(obj)
        except IndexError:
            pass
    return services[1:len(services)-5]
