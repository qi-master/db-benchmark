from optparse import OptionParser
from prettytable import PrettyTable
import re


class JMeterSummary(object):

	class Sample:
		pass
		
	@classmethod
	def _getThroughput(cls, count, time):
		return float(count)/float(time)
	
	@classmethod
	def _getKbs(cls, bytes, time):
		return (lambda l: float(float(sum(l)) / 1024))(bytes) / float(time)
		
	@classmethod
	def _getElapsedTime(cls, start, end):
		return (end - start) / 1000

	@classmethod 
	def _summaryCSV(cls, log):
		#1360953836122,209,Select 1,200,OK,Thread Group 1-1,text,true,53,86
		t_count = dict()
		samples = dict()
		bytes = list()
		 
		logfile = open(log, 'r')
    
		count = 0
		startTime = 0
		endTime = 0
		
		line = logfile.readline()
		while line:
			result = line.split(',')
			if result:
				t_count[result[5]] = 1
				lb = result[2]
				if(result[4] == 'OK'):
			
					bytes.append(int(result[8]))
			
					if(not lb in samples):
						sample = cls.Sample()
						sample.count = 0
						sample.bytes = list()
						samples[lb] = sample
						
						
					samples[lb].count += 1
					samples[lb].bytes.append(int(result[8]))
					
								
				else:
					if(not lb in samples):
						sample = cls.Sample()
						sample.count = 0
						sample.bytes = list()
						samples[lb] = sample
						
					samples[lb].count += 1
					
				
				count += 1
				if(not startTime):
					startTime = result[0]
				else:
					startTime = min(startTime, int(result[0]))
				endTime = max(endTime, int(result[0]))
			  
			line = logfile.readline()
    
		logfile.close()
		
		summary = dict()
		elapsedTime = cls._getElapsedTime(startTime, endTime)
		
		for lb in samples.iterkeys():
			s = cls.Sample()
			s.throughput = cls._getThroughput(samples[lb].count, elapsedTime)
			s.kbs = cls._getKbs(samples[lb].bytes, elapsedTime)
			s.threads = len(t_count)
			summary[lb] = s
		
		s = cls.Sample()
		s.throughput = cls._getThroughput(count, elapsedTime)
		s.kbs = cls._getKbs(bytes, elapsedTime)
		s.threads = len(t_count)
		summary['total'] = s
    
		return summary
	
  
	@classmethod
	def _summaryXML(cls, log):
		
		t_count = dict()
		samples = dict()
		bytes = list()
		reg_ex=r"<sample t=\"(.*)\" lt=\"(.*)\" ts=\"(.*)\" s=\"(.*)\" lb=\"(.*)\" rc=\"(.*)\" rm=\"(.*)\" tn=\"(.*)\" dt=\"(.*)\" by=\"(.*)\"/>"
		sample_regexp = re.compile(reg_ex)
    
		logfile = open(log, 'r')
    
		count = 0
		startTime = 0
		endTime = 0
		
		line = logfile.readline()
		while line:
			result = sample_regexp.search(line)
			if result:
				t_count[result.group(8)] = 1
				lb = result.group(5)
				if(result.group(7) == 'OK'):
			
					bytes.append(int(result.group(10)))
			
					if(not lb in samples):
						sample = cls.Sample()
						sample.count = 0
						sample.bytes = list()
						samples[lb] = sample
						
						
					samples[lb].count += 1
					samples[lb].bytes.append(int(result.group(10)))
					
								
				else:
					if(not lb in samples):
						sample = cls.Sample()
						sample.count = 0
						sample.bytes = list()
						samples[lb] = sample
						
					samples[lb].count += 1
					
				
				count += 1
				if(not startTime):
					startTime = result.group(3)
				else:
					startTime = min(startTime, int(result.group(3)))
				endTime = max(endTime, int(result.group(3)))
			  
			line = logfile.readline()
    
		logfile.close()
		
		summary = dict()
		elapsedTime = cls._getElapsedTime(startTime, endTime)
		
		for lb in samples.iterkeys():
			s = cls.Sample()
			s.throughput = cls._getThroughput(samples[lb].count, elapsedTime)
			s.kbs = cls._getKbs(samples[lb].bytes, elapsedTime)
			s.threads = len(t_count)
			summary[lb] = s
		
		s = cls.Sample()
		s.throughput = cls._getThroughput(count, elapsedTime)
		s.kbs = cls._getKbs(bytes, elapsedTime)
		s.threads = len(t_count)
		summary['total'] = s
    
		return summary
	
	@classmethod
	def summary(cls, log, format="csv"):
		if format == "csv":
			return cls._summaryCSV(log)
		else:
			return cls._summaryXML(log)
	
	@classmethod
	def printSummary(cls, summary, file=None):
		if file:
			f = open(file, 'w')
			for lb in summary.iterkeys():
				f.write("%s;%d;%f;%f\n" % (lb, summary[lb].threads, summary[lb].throughput, summary[lb].kbs))
		else:
			table = PrettyTable()
			table.set_field_names(["sampler", "#threads", "throughput", "kbs"])
			for lb in summary.iterkeys():
				table.add_row([lb, summary[lb].threads, summary[lb].throughput, summary[lb].kbs])
			table.printt()
			
        
	@classmethod
	def clear(cls, log):
		logfile = open(log, 'w')
		logfile.close()
  
  
  
if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i", "--jtlfile", dest="jtlfile", help = "jmeter jtl file name")
	parser.add_option("-f", "--format", dest="format", help = "jmeter jtl file format(default: csv)", default="csv")
	parser.add_option("-o", "--csvfile", dest="csvfile", help = "csv file name", default=None)
	parser.add_option("-c", "--clear", action="store_true", dest="clear", help = "clear jmeter jtl file", default=False)

	(opts, args) = parser.parse_args()
  
	if opts.jtlfile is None:
		parser.print_help()
		exit(-1)
  
	if opts.clear:
		JMeterSummary.clear(opts.jtlfile)
		exit(0)
    
	summary = JMeterSummary.summary(opts.jtlfile, opts.format)  
	JMeterSummary.printSummary(summary, opts.csvfile)
  
