#import simplejson
import json
import sys
import time
from optparse import OptionParser

class JSONToCSVConverter(object):

       
    def __init__(self, json, csv):
        self.__csv = csv
        self.__json = json
    
    @classmethod
    def convert(cls, jsonfile, csvfile):
        start = time.time()
        
        infile = open(jsonfile, 'r')
        outfile = open(csvfile, 'w')

        string = ""
        id = 0
        line = infile.readline()
        while line:

            data = json.loads(line)
            string = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (
                str(int(data.get("time", 0))),
                data.get("event", ""), 
                str(int(data.get("uid", 0))), 
                str(int(data.get("pid", 0))),
                str(int(data.get("delta.cinematicket", 0))),
                str(int(data.get("delta.cR", 0))),
                str(int(data.get("delta.cV", 0))),
                str(data.get("delta.water", 0)),
                data.get("field.item", ""),
                str(data.get("product", "0")),
                str(int(data.get("productAmount", 0))),
                data.get("sid", ""),
                data.get("tid", ""),
                data.get("iid", ""),
                str(int(data.get("delta.ep", 0))),
                data.get("generator", "")
                )
                    
            
            outfile.write(string)
            line = infile.readline()
            id = id + 1

        infile.close()
        outfile.close()

        end = time.time()
        print "%d records converted" % id
        print "Conversion time: " + (str)(end - start) + " sec"
        print "DONE"

        JSONToCSVConverter.generate_ctl("BENCHMARK", "FARM", csvfile.split('.')[0], "badfile.err");

    @classmethod
    def generate_ctl(cls, schema, table, csvfile, badfile):
        """Generate CTL File for Batch-Loading into Database"""
        print "Generating CTL..."
        sctl = """import data into table %s.%s
                    from '%s.csv'
                    record delimited by '\n'
                    fields delimited by ';'
                    optionally enclosed by '"'
                    error log '%s'"""
       

        ctlfile = open('%s.ctl' % (csvfile), 'w')
        ctlfile.write(sctl % (schema, table, csvfile, badfile))
        ctlfile.close()
        
        badfile = open(badfile, 'w')
        badfile.close()
       

        
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="injson", help="input json file name")
    parser.add_option("-o", "--output", dest="outcsv", help="output csv file name")

    (opts, args) = parser.parse_args()
    if (opts.injson is None) or (opts.outcsv is None):
        parser.print_help()
        exit(-1)

    JSONToCSVConverter.convert(opts.injson, opts.outcsv)
