from dbconnector import DBConnector
import urllib
import urllib2

class HyriseConnector(DBConnector):
    """Connector for HYRISE"""



    def fireQuery(self, query, queryid=0):

        values = {'query': query}
        data = urllib.urlencode(values)
        req = urllib2.Request("%s:%d" % (self.host, self.port), data)
        response = urllib2.urlopen(req)

        result = response.read()

        try:
            return json.loads(result, encoding='latin-1')
        except ValueError:
            return None
       


  






    

  

      
