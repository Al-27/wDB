from flask import Blueprint

api_b = Blueprint('api_b',__name__, url_prefix='/api') 
from api.table_ops import *