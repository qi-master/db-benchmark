from util.json_to_csv import JSONToCSVConverter
from optparse import OptionParser
from connector_factory import ConnectorFactory


@classmethod
def cleartbl(cls, tables):
	try:
		for table in tables:
			execute('''DELETE FROM "%s"''' %(table))
	finally:

@classmethod
def load_to_hana(cls, dir):
	
	start = time.time()
	
	connector = ConnectorFactory.getconnector()
	stmt = connector.get_load_stmt()
	connector.fireQuery(stmt)
	
	end = time.time()
	
		
		
		

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-d", "--directory", dest=