from optparse import OptionParser
import re


class JMeterSummary(object):
  
  @classmethod
  def summary(cls, log, exectime):
    bytes = list()
    
    reg_ex=r"<httpSample t=\"(.*)\" lt=\"(.*)\" ts=\"(.*)\" s=\"(.*)\" lb=\"(.*)\" rc=\"(.*)\" rm=\"(.*)\" tn=\"(.*)\" dt=\"(.*)\" by=\"(.*)\"/>"
    sample_regexp = re.compile(reg_ex)
    
    logfile = open(log, 'r')
    
    count = 0
    
    line = logfile.readline()
    while line:
      result = sample_regexp.search(line)
      if result:
        if (result.group(5).find('DS') != -1 or result.group(5).find('PDP') != -1 or result.group(5).find('PEP') != -1) and result.group(7) == 'OK':
          count += 1
          bytes.append(int(result.group(10)))
        
      line = logfile.readline()
    
    logfile.close()
    
    throughput = float(count) / float(exectime)
    kbs = count * (lambda l: float(sum(l)) / (float(len(l)) * 1024) if len(l) > 0 else 0)(bytes) / float(exectime)
    
    return (throughput, kbs)
        
  @classmethod
  def clear(cls, log):
    logfile = open(log, 'w')
    logfile.close()
  
  
  
if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-j", "--jtlfile", dest="jtlfile", help = "jmeter jtl file name")
  parser.add_option("-c", "--clear", action="store_true", dest="clear", help = "clear jmeter jtl file", default=False)
  
  (opts, args) = parser.parse_args()
  
  if opts.jtlfile is None:
    parser.print_help()
    exit(-1)
  
  if opts.clear:
    JMeterSummary.clear(opts.jtlfile)
    
  print JMeterSummary.summary(opts.jtlfile, 30)  
  
