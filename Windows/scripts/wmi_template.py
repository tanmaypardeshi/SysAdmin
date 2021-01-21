import wmi
import pythoncom
import json
from operator import attrgetter

def wmi_controller(req):
    try:
        win_class, projection, match, query, func, args = attrgetter('win_class', 'projection', 'match', 'query', 'func', 'args')(req)
        pythoncom.CoInitialize()
        computer = wmi.WMI()

        is_pr = isinstance(projection, list)
        is_match = isinstance(match, dict)

        if isinstance(query, str):
            wmi_objs = computer.query(query)
        else:
            projection = projection if is_pr else []
            match = match if is_match else {}
            wmi_objs = getattr(computer, win_class)(projection, **match)

        arr = []
        for wo in wmi_objs:
            properties, methods = [vars(wo)[k] for k in ('properties', 'methods')]
            res = {}

            for prop in properties:
                res[prop] = getattr(wo, prop)

            if isinstance(func, str) and func in methods:
                try:
                    args = args if isinstance(args, list) else []
                    response_code = getattr(wo, func)(*args)[0]
                except Exception as e:
                    response_code = str(e)
                finally:
                    res["ResponseCode"] = response_code

            arr.append(res)

        return arr
    except Exception as e:
        return str(e)

# pythoncom.CoInitialize()

# computer = wmi.WMI()

# win_class = 'Win32_Service'
# projection = None
# is_p_list = isinstance(projection, list)
# match = None
# is_c_dict = isinstance(match, dict)
# query = None
# func = None
# args = []

# if isinstance(query, str):
#     res = computer.query(query)
# elif is_p_list and is_c_dict:
#     res = getattr(computer, win_class)(projection, **match)
# elif is_p_list:
#     res = getattr(computer, win_class)(projection)
# elif is_c_dict:
#     res = getattr(computer, win_class)(**match)
# else:
#     res = getattr(computer, win_class)()

# for r in res:
#     properties, methods = [vars(r)[k] for k in ('properties', 'methods')]
#     output = {}
#     for prop in properties:
#         output[prop] = getattr(r, prop) # Converting instance of _wmi_object to dictionary for JSON serializability

#     if func is not None and func in methods:
#         response_code = None
#         try:
#             response_code = getattr(r, func)(*args)[0]
#         except Exception as e:
#             response_code = str(e)
#         finally:
#             output["ResponseCode"] = response_code

#     print(json.dumps(output, indent=2))

# pythoncom.CoUninitialize()
