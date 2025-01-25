from flask import make_response, abort, jsonify, request
from . import api_b
from db import db_e
from db.utils import to_obj, rows_to_list 

@api_b.route('/tables',methods=['GET'])
def get_tables():
    return jsonify( db_e.get_tables_schema() )

@api_b.route('/table/<table_name>', methods=['GET'],strict_slashes=False)
def select_table(table_name):
    rows = db_e.switch_to_table(table_name)
    return jsonify(rows_to_list(rows))

@api_b.route('/table', methods=['POST'],strict_slashes=False)
@api_b.route('/table/<data>', methods=['POST'],strict_slashes=False)
def add_table(data=None):
    obj = data
    if obj is not None:
        obj = to_obj(data)
    else:
        obj = request.json
        print(request.json)
        print(request.data)
    try:
        db_e.new_table(**obj)
    except Exception as e:
        return {'error': str(e)},401
    return jsonify({'res':'ok'})

@api_b.route('/table', methods=['DELETE'],strict_slashes=False, defaults={'table_name':None})
@api_b.route('/table/<table_name>', methods=['DELETE'],strict_slashes=False)
def drop_table(table_name):
    try:
        print(table_name)
        db_e.drop_table(table_name) 
    except Exception as e:
        return {'error': str(e)},401
    return jsonify({'res':'ok'})