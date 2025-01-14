from flask import make_response, abort, jsonify, request
from . import db_e, api_b
from db.utils import to_obj, rows_to_list
from flask import Blueprint

@api_b.route('/tables',methods=['GET'])
def get_tables():
    return jsonify( db_e.get_tables_schema() )

@api_b.route('/table/<table_name>', methods=['GET'],strict_slashes=False)
def select_table(table_name):
    rows = db_e.switch_to_table(table_name)
    return jsonify(rows_to_list(rows))

@api_b.route('/table/<data>', methods=['POST'],strict_slashes=False)
def add_table(data):
    obj = to_obj(data)
    db_e.new_table(**obj)
