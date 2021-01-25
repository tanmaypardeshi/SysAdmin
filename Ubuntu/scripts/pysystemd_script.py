import pysystemd


def pysystemd_script(req):
    try:
        try:
            class_name = getattr(pysystemd, req.class_name)(req.dargs)
            return getattr(class_name, req.func)()
        except Exception as e:
            print(str(e))
            class_name = getattr(pysystemd, req.class_name)()
            return getattr(class_name, req.func)()
    except Exception as e:
        return str(e)
