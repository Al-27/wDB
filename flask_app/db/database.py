from sqlalchemy import Column, String, Integer, Float, Boolean, \
                        DateTime, Date, Time, MetaData, Table ,\
                        create_engine, Engine, make_url, URL
import json

class DataBaseCreator:
    types = {
	'str': String,
	'int': Integer,
	'float': Float,
	'bool': Boolean,
	'datetime': DateTime,
	'date': Date,
	'time': Time
	}
    metadata: MetaData = None

    def __init__(self, mt):
        self.metadata = mt
        pass

    def create_table(self, table_name: str, col_data: dict):
        """
        """
        cols = self.init_cols(col_data)
        return Table(table_name, self.metadata, *cols)

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


class DBEngine():
    __creator: DataBaseCreator= None
    __engine: Engine = None
    __metadata: MetaData = None
    cur_Table: Table = None

    def __init__(self, db_e='sqlite', user=None, pw=None, db_n=None):
        url = URL.create(db_e, username=user, password=pw, database=db_n)
        self.__engine = create_engine(url)
        self.__metadata = MetaData()
        #reflect to get all existing tables within db_e
        self.__metadata.reflect(bind=self.__engine)
        self.__creator = DataBaseCreator(self.__metadata)
    
    def get_tables(self):
        """
        [{ tab_name : str, cols: [...{colname: str, type: str, nullable: bool, pk: bool, unique: bool} ] }]
        """ 
        tables_data = []
        for tab_n, table in self.__metadata.tables.items():
            tables_data.tab_name = tab_n
            tables_data.cols = []
            for col_n, col in table.columns.items():
                tables_data.cols.append( {'colname': col_n, 'type': str(col.type.python_type), 'nullable': col.nullable, \
                                           'pk': col.primary_key, 'unique': col.unique} )
        return json.dumps(tables_data)

    def new_table(self, **table):
        """
        {table_name: [{colname: str, type: str, nullable: bool, pk: bool, unique: bool}]}
        """
        tbl_n, tbl_d = list(table.keys())[0], list(table.values())[0]
        nTable = self.__creator.create_table(tbl_n,tbl_d)
        nTable.create(self.__engine,True)
        self.cur_Table = nTable

    def drop_table(self, table: str):
        table_r = self.__metadata.tables[table]
        table_r.drop(self.__engine)

    def insert(self, row_data: dict):
        if row_data and not row_data == {}:
            con = self.__engine.connect()
            st = self.cur_Table.insert().values(**row_data)
            con.execute(st) 
            con.commit()
            con.close()
    
    def select(self, stmt):
        con = self.__engine.connect()
        res = con.execute(stmt) 
        con.commit()
        con.close()
        return res