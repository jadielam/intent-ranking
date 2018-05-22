def clean_entry(entry):
    i = 0
    j = -1
    start = 0
    end = len(entry)

    while entry[i] == "\"":
        start += 1
        i += 1

    while entry[j] == "\"":
        end -= 1
        j -= 1

    return entry[start: end]

def _lowercase(obj):
    """ Make dictionary lowercase """
    if isinstance(obj, dict):
        t = type(obj)()
        for k, v in obj.items():
            if type(k) is not int:
                t[k.lower()] = _lowercase(v)
            else:
                t[k] = _lowercase(v)
        return t
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(_lowercase(o) for o in obj)
    elif isinstance(obj, basestring):
        return obj.lower()
    else:
        return obj
