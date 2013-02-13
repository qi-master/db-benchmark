import ConfigParser
from hana_connector import HanaConnector


class ConnectorFactory(object):


	@classmethod
	getconnector(cls):

		config = ConfigParser.RawConfigParser()
		config.read('config.cfg')

		db = config.get('General', 'db').ascii_uppercase

		if (db == "HANA"):
			host = config.get('HANA', 'host')
			port = config.getint('HANA', 'port')
			user = config.get('HANA', 'user')
			password = config.get('HANA', 'password')
			schema = config.get('HANA', 'schema')
			return HanaConnector(host, port, user, password, schema)
		
		if (db == "HYRISE"):
			host = config.get('HYRISE', 'host')
			port = config.getint('HYRISE', 'port')
			return HyriseConnector(host, port)

