from hdbcli import dbapi
from dbconnector import DBConnector

class HanaConnector(DBConnector):
    """Connector for HANA"""


    def getconn(self):
        """Convenient method to get connection"""
        #hdbport = int('3%s15' % Settings.hdbinstancenum)
        con = dbapi.connect(address = self.host, \
            port = self.port, \
            user = self.username, \
            password = self.password, \
            autocommit = True)
        if self.schema:
            cur = con.cursor()
            try:
                cur.execute('ALTER SESSION SET CURRENT_SCHEMA = %s' % self.schema)
                return con
            except dbapi.Error, err:
                cur.close()
                con.close()
                cur = None
                raise err
            finally:
                if cur:
                    cur.close()
        else:
            return con


    def fireQuery(self, query, queryid=0):
        try:
            try:
                con = cls.getconn()
                cur = con.cursor()
                cur.execute(query)
            except dbapi.Error, err:
                print err
        finally:
            cur.close()
            con.close()

    # @classmethod
    # def fireSQLStatementsFromFile(cls, filename):
    #     file = open(filename, 'r')
    #     statement = file.readline()
    #     while statement:
    #         cls.fireSQLStatement(statement)
    #         statement = file.readline()




  






    

  

      
