from sqlalchemy import Column, String, Integer, Float, Boolean, \
                        DateTime, Date, Time, MetaData, Table ,\
                        create_engine, Engine, make_url, URL, \
                        Connection, Null,select
from sqlalchemy.orm import Session
import json

class TableEngine:
    types = {
	'str': String,
	'int': Integer,
	'float': Float,
	'bool': Boolean,
	'datetime': DateTime,
	'date': Date,
	'time': Time
	}
    __metadata: MetaData = None

    def __init__(self, engine):
        self.__metadata = MetaData()
        self.__metadata.reflect(bind=engine)
        pass

    def create_table(self, table_name: str, col_data: dict):
        """
        """
        cols = self.init_cols(col_data)
        return Table(table_name, self.__metadata, *cols)
    
    def drop(self, table_nm: str, engine: Engine):
        table_r = self.__metadata.tables[table_nm]
        table_r.drop(engine)

    def get_tables(self):
        return self.__metadata.tables

    def init_cols(self, col_data: list[dict]):
        """
        [{colname: str, type: str, nullable: bool, pk: bool, unique: bool}]
        """ 
        cols = []

        if col_data: 
            for column in col_data:
                cols.append(Column(column['colname'], self.types[column['type']], nullable=column['nullable'] ,\
                                    primary_key=column['pk'], unique=column['unique']))
        return cols

    
    def insert(self, conn: Connection, table: Table, row_data: dict):
        if row_data and not row_data == {}:
            st = table.insert().values(**row_data)
            conn.execute(st) 
            conn.commit()
    
    def select(self, sess: Session, table_nm, all: bool=False):
        """
        @all: get all rows, (def: get first)
        TODO: create a func in utils to convert rows to list, to be 'jsonable'
        """
        table = self.__metadata.tables[table_nm]
        stmt = select(table)
        res = sess.execute(stmt).all()
        if not all and len(res) > 0:
            res = res[0] 
        return res



class DBEngine():
    __tableE: TableEngine= None
    __engine: Engine = None
    __session: Session = None
    cur_Table: Table = None

    def __init__(self, db_e='sqlite', user=None, pw=None, db_n=None):
        url = URL.create(db_e, username=user, password=pw, database=db_n)
        self.__engine = create_engine(url) 
        self.__tableE = TableEngine(self.__engine)
        self.__session = Session(self.__engine)

    def new_table(self, **table):
        """
        {table_name: [{colname: str, type: str, nullable: bool, pk: bool, unique: bool}]}
        """
        tbl_n, tbl_d = list(table.keys())[0], list(table.values())[0]
        self.cur_Table = self.__tableE.create_table(tbl_n,tbl_d)
        self.cur_Table.create(self.__engine,True)

    def drop_table(self, table: str):
        table_r = self.__tableE.drop(table, self.__engine)
        table_r.drop(self.__engine)
    
    def get_tables_schema(self):
        """
        { tabl_name : {tabl_name : str, cols: [...{colname: str, type: str, nullable: bool, pk: bool, unique: bool} ] }}
        """ 
        tables_data = {}
        for tab_n, table in self.__tableE.get_tables().items():
            tables_d = {}
            tables_d['tabl_name'] = tab_n
            tables_d['cols'] = []
            for col_n, col in table.columns.items():
                tables_d['cols'].append( {'colname': col_n, 'type': str(col.type.python_type.__name__), 'nullable': col.nullable, \
                                           'pk': col.primary_key, 'unique': col.unique} )
            tables_data[tab_n] = tables_d
        return tables_data

    def switch_to_table(self, table_n: str):
        self.cur_Table = self.__tableE.get_tables()[table_n]
        return self.get_row()

    def get_table_data(self):
        """
        --> [{ tabl_name : [...{col_1,col_2...,col_n} ] }]
        """
        if self.cur_Table is not None:
            pass
            

    def add_row(self, row_data: dict, table_n: str=None):
        """
        TODO: return added row
        """
        if row_data and not row_data == {}:
            con = self.__engine.connect()
            table = self.cur_Table
            
            if table_n:
                table = self.__tableE.get_tables()[table_n]
                
            self.__tableE.insert(con, table, row_data)
            con.close()
    
    def get_row(self, table_n: str=None, x=1):
        """
        TODO: retrieve x rows using limit
        """ 
        table = self.cur_Table.name 
        if table_n != None :
            table = table_n
            
        res = self.__tableE.select(self.__session, table, True) 
        return res