from json import dumps, loads

def rows_to_list(rows):
    if type(rows) is not list:
        return list(rows)
    lrow = []
    for r in rows:
        lrow.append(list(r))
    return lrow

def to_json(obj):
    return dumps(obj)

def to_obj(jsn):
    return loads(jsn)
 