from optparse import OptionParser
from jmetersummary import JMeterSummary
from sqlutil import SQLUtil
import os


import time
int(time.time())


parser = OptionParser()
parser.add_option("-j", "--jmeterdir", dest="jmeterdir", help = "jmeter directory")
parser.add_option("-t", "--jmetertestplan", dest="jmetertestplan", help = "jmeter testplan")

parser.add_option("-s", "--server", dest="server", help = "hdbaddons server")
parser.add_option("-p", "--port", dest="port", help = "hdbaddons port") 
parser.add_option("-r", "--remoteservers", dest="remoteservers", help="remote jmeter servers separated by ,")

parser.add_option("-g", "--generatordir", dest="generatordir", help = "policyDBgenerator directory")

parser.add_option("-l", "--jtlfile", dest="jtlfile", help = "jmeter jtl file")
parser.add_option("-o", "--outputfile", dest="outputfile", help = "output file")
  
(opts, args) = parser.parse_args()
  
if opts.jmeterdir is None \
or opts.server is None \
or opts.port is None \
or opts.generatordir is None \
or opts.jmetertestplan is None \
or opts.jtlfile is None \
or opts.outputfile is None:
  parser.print_help()
  exit(-1)
  
 
 
threads = (1, 5, 10, 50, 100)

json_csv_converter = """python %s/json_csv_converter.py -i %s -o %s"""
json_csv_converter_clean = """python %s/json_csv_converter -c"""



if opts.remoteservers is None:
  sjmeter = """%s/%s -n -t %s -l %s -Jthreads=%s -Jduration=%s -Jhost=%s -Jport=%s %s"""
else:
  sjmeter = """%s/%s -n -t %s -l %s -Gthreads=%s -Gduration=%s -Ghost=%s -Gport=%s %s"""



resultsfile = open(opts.outputfile, 'w')
resultsfile.write("#requests;throughput/sec;KB/sec;\n")

# print "----- Generating %s policies with hitrate %s into DB -----" % (p, h)
# if opts.jmetertestplan.find('ds') != -1 or opts.jmetertestplan.find('pep') != -1:
#   os.system(spolicydbgenerator %(opts.generatordir, p, str(h) + ' -a'))
# else:
#   os.system(spolicydbgenerator %(opts.generatordir, p, h))
# print "----- Loading policies into DB -----"
# SQLUtil.loadPolicies(os.getcwd())
for t in threads:
  
  print "----- Running testplan with %s threads -----" % t
  os.system(sjmeter % (opts.jmeterdir, "bin/jmeter", opts.jmetertestplan, opts.jtlfile, t, "100", opts.server, opts.port, "" if opts.remoteservers is None else "-R " + opts.remoteservers))
  print "----- Testrun finished -----"
  print "----- Calculating summary -----"
  

  throughput, kbs = JMeterSummary.summary(opts.jtlfile, 100)
  JMeterSummary.clear(opts.jtlfile)
  
  resultsfile.write("%s;%s;%s;\n" %(t, throughput, kbs))
  resultsfile.flush()

print "----- Cleaning up -----"
#SQLUtil.clearUsers()
#os.system(spolicydbgeneratorclean %(opts.generatordir))          
resultsfile.close()

try:
  os.remove(opts.jtlfile)
  os.remove('jmeter.log')
except Exception, err:
  print 'cannot remove file'
print '----- Results saved to %s -----' % opts.outputfile
