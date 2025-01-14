from flask import Blueprint
from db import DBEngine

api_b = Blueprint('api_b',__name__, url_prefix='/api')
db_e = DBEngine()

from api.table_ops import *