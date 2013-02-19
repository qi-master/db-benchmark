import matplotlib.pyplot as plt
import numpy as np
import os
import re
from optparse import OptionParser



class Plotter(object):

	@classmethod
	def plotTotals(cls, testrundir):
		pass
	
	@classmethod
	def plotSample(cls, testrundir, lb=None):
		cpool = ['#708090', 'red', '#0000cd', '#ffd700', 'cyan', '#9400d3']
		
		dir = os.path.dirname(os.path.abspath(__file__)) + os.path.normcase('/') + 'results' + os.path.normcase('/') + testrundir
		files = [f for f in os.listdir(dir) if re.match(r'[0-9]+-[0-9]+\.csv',f)]
		
		threads = dict()
		sampler_lb = list()	
		
		data_throughput = list()
		data_kbs = list()
		threads = list()
		
		sc = 0
		
		first = True
		for f in files:
			file = open(dir + os.path.normcase('/') + f, 'r')
			
			threads.append(int(f.split('.')[0].split('-')[0]))

			line = file.readline()
			while line:
				result = line.split(';')
				
				if first:
					sampler_lb.append(result[0])
					sc += 1
					
				data_throughput.append(result[2])
				data_kbs.append(result[3])
				
				line = file.readline()
				
			
			first = False
			
		locs = np.array(threads)
		
		fig = plt.figure()
		ax = plt.subplot(111)
		
		for i in range(sc):
			data_throughput_t = list()
			for j in range(len(threads)):
				data_throughput_t.append(float(data_throughput[j*sc + i]))

			ax.plot(locs, data_throughput_t, color=cpool[i], label = sampler_lb[i]);
		
		box = ax.get_position()
		
		ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.9])
		
		ax.grid(True)
		
		plt.title('Throughput')
		plt.ylabel('Throughput')
		plt.xlabel('#threads')
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09), fancybox=True, shadow=True, ncol=3)
		
		plt.show()

	
	@classmethod
	def plotAll(cls, testrundir, lb=None):
	
		cpool = ['#708090', 'red', '#0000cd', '#ffd700', 'cyan', '#9400d3']	
		dir = os.path.dirname(os.path.abspath(__file__)) + os.path.normcase('/') + 'results' + os.path.normcase('/') + testrundir
		files = [f for f in os.listdir(dir) if re.match(r'[0-9]+-[0-9]+\.csv',f)]
		
		threads = dict()
		sampler_lb = list()	
		
		data_throughput = list()
		data_kbs = list()
		threads = list()
		
		sc = 0
		
		first = True
		for f in files:
			file = open(dir + os.path.normcase('/') + f, 'r')
		
			threads.append(int(f.split('.')[0].split('-')[0]))
			
			line = file.readline()
			while line:
				result = line.split(';')
				
				if first:
					sampler_lb.append(result[0])
					sc += 1
					
				data_throughput.append(result[2])
				data_kbs.append(result[3])
				
				line = file.readline()
				
			first = False
		
		locs = np.arange(1, len(threads) + 1)
		
		width = float(len(locs))/ (len(threads)*sc*1.5)
		
		fig = plt.figure()
		ax = plt.subplot(111)
		
		for i in range(sc):
			data_throughput_t = list()
			for j in range(len(threads)):
				data_throughput_t.append(float(data_throughput[j*sc + i]))
				
			ax.bar(locs + i*width, data_throughput_t, width=width, color=cpool[i], label = sampler_lb[i]);
		
		box = ax.get_position()
		
		ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.9])
		
		plt.xticks(locs + (float(sc)/len(threads))*width, sorted(threads));
		ax.grid(True)
		
		plt.title('Throughput')
		plt.ylabel('Throughput')
		plt.xlabel('#threads')
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09), fancybox=True, shadow=True, ncol=3)
		
		plt.show()

		
if __name__ == '__main__':	
parser = OptionParser()
	parser.add_option("-d", "--dir", dest="dir", help = "directory with testrun results")
	
	(opts, args) = parser.parse_args()
  
	if opts.dir is None:
		parser.print_help()
		exit(-1)
  
	
	Plotter.plotAll('results')
			
			
				
			
				
		