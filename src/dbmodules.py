import os
import sys
import sqlalchemy as db
from sqlalchemy.exc import ProgrammingError
scriptPath = os.path.realpath(os.path.dirname('frontend/logsetup/'))
if scriptPath not in sys.path:
    sys.path.append(scriptPath)

sys.path.append('../frontend')
import frontend.logsetup.log_setup as log_setup

logger = log_setup.logging.getLogger(__name__)
logger_r = log_setup.logging.getLogger('db')


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
            logger_r.debug("Database instance created")
        except Exception as b:
            logger_r.debug("Conection to Database Failed")
            logger.error(f"Conection to Database Failed - {b}")

    def fetchByTable(self, t_name: str) -> list:
        """fetchByTable Method to print all the rows from a specific table

        :param t_name: name of the table to be fetched
        :type t_name: str
        """
        # Run selected query and print all the outputs
        list_toreturn = []
        try:
            fetchQuery = self.connection.execute(f"SELECT * FROM {t_name}")
            for data in fetchQuery.fetchall():
                list_toreturn.append(data)
            logger_r.debug("all rows returned")
            return list_toreturn
        except ProgrammingError as a:
            logger.error(f"Wrong Table Name - {a}")
            logger_r.debug(f"Wrong Table Name - {a}")

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
                logger_r.debug(f"Data inserted succesfully")
            return True
        except ProgrammingError as a:
            logger.error(f"ProgrammingError  - {a}")
            logger_r.debug(f"ProgrammingError - {a}")
        except Exception as a:
            logger.error(f"Dataframe error to_sql  - {a}")
            logger_r.debug(f"Dataframe error to_sql - {a}")

            return False

    def fetchByQuery(self, query: str) -> list:
        """fetchByQuery Method to print all the rows from a specific query

        :param query: query in sql sintax 
        :type t_name: str
        :return: list with all the returned rows
        :rtype: list
        """
        # Run selected query and print all the outputs
        list_toreturn = []
        try:
            fetchQuery = self.connection.execute(query)
            for data in fetchQuery.fetchall():
                list_toreturn.append(data)
            logger_r.debug("All rows returned")
            return list_toreturn
        except ProgrammingError as a:
            logger.error(f"ProgrammingError  - {a}")
            logger_r.debug(f"ProgrammingError - {a}")

    def dinorderquery(self, table: str, **kwargs: dict) -> str:
        """dinorderquery Method to set a sql query with order conditions

        :param table: sql query
        :type table: str
        :return: sql query + order conditions
        :rtype: str

        Usage example dinorderquery("Select * from a",column1 = 'ASC', column3 = 'DESC')


        """
        table = table + " order by "
        for column, value in kwargs.items():
            table = table + column + " " + value + ","
            logger_r.debug(f"dinorderquery - columns {column} - values {value}")
        return table[:-1]

    def dinfilterqueryand(self, table: str, **kwargs: dict) -> str:
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

        for column, value in kwargs.items():
            table = table + column + " " + value + "AND "
            logger_r.debug(f"dinfilterqueryand - columns {column} - values {value}")
        return table[:-4]

    def dinfilterqueryor(self, table: str, **kwargs: dict) -> str:
        """dinfilterqueryor Method to set a sql query with (OR) filtering conditions

        :param table: sql query
        :type table: str
        :return: sql query + filter conditions
        :rtype: str

        Usage example dinfilterqueryor("Select * from a",column1 = '>5 ',column4 = '= \'texttocompair \'')
        """

        # If the table is the result of a query will add the ()
        if "select" in table.lower():
            table = "select * from ("+table + ") as b Where "

        # If the table is a ddbb table will remove the () chars
        else:
            table = "select * from "+table + " as b Where "

        for column, value in kwargs.items():
            table = table + column + " " + value + "OR "
            logger_r.debug(f"dinfilterqueryor - columns {column} - values {value}")
        return table[:-3]
