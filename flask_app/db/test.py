from database import DBEngine
import json as j
dbEnging = DBEngine()
dbEnging.new_table(**{'test': [{'colname': 'id', 'type': 'int', 'nullable': None, 'pk': True, 'unique': None},\
                             {'colname': 'name', 'type': 'str', 'nullable': None, 'pk': None, 'unique': None},\
                             {'colname': 'title', 'type': 'str', 'nullable': True, 'pk': None, 'unique': None}]})
dbEnging.new_table(**{'table_x': [{'colname': 'id', 'type': 'int', 'nullable': None, 'pk': True, 'unique': None},\
                             {'colname': 'oop', 'type': 'str', 'nullable': None, 'pk': None, 'unique': None},\
                             {'colname': 'date_c', 'type': 'date', 'nullable': None, 'pk': None, 'unique': None}]})
print(dbEnging.cur_Table)
print(dbEnging.cur_Table.columns)
print(dbEnging.switch_to_table('test')) 
dbEnging.add_row({'name':'John' })
dbEnging.add_row({'name':'John','title':'Tec'})
dbEnging.add_row({'name':'John','title':'IT'})
print(dbEnging.switch_to_table('test')) 
