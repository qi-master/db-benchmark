import abc


class DBConnector(object):
	"""Abstract DB-Connector.

	attributes:
	"""

	__metaclass__ = abc.ABCMeta


	def __init__(self, host, port, username=None, password=None, schema=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.schema = schema


	@abc.abstractmethod
	def fireQuery(self, query, queryid=0):
		"""Execute Query"""
		return 

