import psutil

def psutil_controller(req):
    try:
        args = req.dargs if isinstance(req.dargs, dict) else {}
        result = getattr(psutil, req.func)(**args)
        try:
            result = result._asdict()
        except Exception as e:
            pass
        return result
    except Exception as e:
        return str(e)