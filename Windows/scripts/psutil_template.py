import psutil

# fn = 'cpu_times'
# dargs = {}

# print(getattr(psutil, fn)(**dargs))

def psutil_controller(req):
    try:
        args = req.dargs if isinstance(req.dargs, dict) else {}
        return getattr(psutil, req.func)(**args)
    except Exception as e:
        return str(e)