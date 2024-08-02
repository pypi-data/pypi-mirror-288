class DB_Config(object):
    def __init__(self, server,database,user=None,password=None,trust=False,trust_server_certificate=False,port=1433,driver="ODBC Driver 17 for SQL Server"):
        self.driver=driver
        self.server=server
        self.trust=trust
        self.trust_server_certificate=trust_server_certificate
        self.user=user
        self.password=password
        self.database=database
        self.port=port
