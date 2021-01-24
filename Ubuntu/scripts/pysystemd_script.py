import pysystemd


def pysystemd_script(req):
    try:
        class_name = getattr(pysystemd, req.class_name)()
        return getattr(class_name, req.func)(**req.dargs if isinstance(req.dargs, dict) else {})
    except Exception as e:
        return str(e)
