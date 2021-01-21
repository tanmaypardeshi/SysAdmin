import psutil


def psutil_controller(req):
    try:
        return getattr(psutil, req.func)(**req.dargs if isinstance(req.dargs, dict) else {})
    except Exception as e:
        return str(e)
