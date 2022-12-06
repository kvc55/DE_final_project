import sqlalchemy as db


class Database():
    """
    Class Database, its used to stabish the connection to the postgresql server

    """

    def __init__(self, user: str, password: str, host: str, dbname: str) -> object:
        """__init__ Instance method to create a database object

        :param user: ddbb username
        :type user: str
        :param password: ddbb password
        :type password: str
        :param host: ddbb host
        :type host: str
        :param dbname: name of the database
        :type dbname: str
        :return: database object
        :rtype: object
        """
        self.user = user
        self.password = password
        self.host = host
        self.dbname = dbname
        # Create engine and connection
        try:
            self.engine = db.create_engine(f"postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}")
            self.connection = self.engine.connect()
            print("Db instance created")
        except Exception as b:
            print(f"Logged connection error {b}")

    def fetchByTable(self, t_name: str) -> None:
        """fetchByTable Method to print all the rows from a specific table

        :param t_name: name of the table to be fetched
        :type t_name: str
        """
        # Run selected query and print all the outputs
        fetchQuery = self.connection.execute(f"SELECT * FROM {t_name}")
        for data in fetchQuery.fetchall():
            print(data)
        print("all rows returned")

    def bulkInsert(self, dfname: object, t_name: str) -> bool:
        """bulkInsert Method to bulk insert a dataframe into a table

        :param dfname: dataframe that contains the data to insert
        :type dfname: object
        :param t_name: table name that is going to be used to insert
        :type t_name: str
        :return: True value if ended successfully , False in case that fails
        :rtype: bool
        """

        # Replace dataframe index by the first column
        dfname = dfname.set_index(dfname.columns[0])
        try:
            with self.engine.begin() as connection:
                dfname.to_sql(t_name, con=connection, if_exists='append')
            return True
        except Exception as a:
            print(f"Error logged {a}")
            return False


    def fetchByQuery(self, query: str) -> None:
        """fetchByQuery Method to print all the rows from a specific query

        :param query: query in sql sintax 
        :type t_name: str
        """
        # Run selected query and print all the outputs
        fetchQuery = self.connection.execute(query)
        for data in fetchQuery.fetchall():
            print(data)
        print("all rows returned")


    def dinorderquery(self, table : str,**kwargs : dict) -> str :
        """dinorderquery Method to set a sql query with order conditions

        :param table: sql query
        :type table: str
        :return: sql query + order conditions
        :rtype: str
        
        Usage example dinorderquery("Select * from a",column1 = 'ASC', column3 = 'DESC')
        
        
        """
        table = table + " order by "
        for column,value in kwargs.items():
            table = table + column + " " + value + ","
        return table[:-1]
        

    def dinfilterqueryand(self, table : str,**kwargs : dict) -> str :
        """dinfilterqueryand Method to set a sql query with (AND) filtering conditions

        :param table: sql query
        :type table: str
        :return: sql query + filter conditions
        :rtype: str

        Usage example dinfilterqueryand("Select * from a",column1 = '>5 ',column4 = '= \'texttocompair \'')

        """
        # If the table is the result of a query will add the ()
        if "select" in table.lower():
            table = "select * from ("+table + ") as a Where "
        
        # If the table is a ddbb table will remove the () chars
        else:
            table = "select * from "+table + " as a Where "

        for column,value in kwargs.items():
            table = table + column + " " + value + "AND "
        return table[:-4]
    
    def dinfilterqueryor(self, table : str,**kwargs : dict) -> str :
        """dinfilterqueryor Method to set a sql query with (OR) filtering conditions

        :param table: sql query
        :type table: str
        :return: sql query + filter conditions
        :rtype: str
    
        Usage example dinfilterqueryand("Select * from a",column1 = '>5 ',column4 = '= \'texttocompair \'')
        """

        
        # If the table is the result of a query will add the ()
        if "select" in table.lower():
            table = "select * from ("+table + ") as b Where "
        
        # If the table is a ddbb table will remove the () chars
        else:
            table = "select * from "+table + " as b Where "

        for column,value in kwargs.items():
            table = table + column + " " + value + "OR "
        return table[:-3] 