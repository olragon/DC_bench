#!/usr/bin/env python
"""
Benchmark datacenter 
1. Network latency (Ping benchmark)
2. Download benchmark

@author
	olragon@gmail.com
@file
	Simple network benchmark
@history
	2011-05-09:	Created
"""
import subprocess, re, urllib2, time, warnings, sys, argparse
warnings.filterwarnings("ignore") # We don't care

ping_time = '10' # Number of ping time
download_size = 0.1 # File size in megabyte (MB)
dcs = {'london1.linode.com': 'http://london1.linode.com/100MB-london.bin',
			'newark1.linode.com': 'http://newark1.linode.com/100MB-newark.bin',
			'atlanta1.linode.com': 'http://atlanta1.linode.com/100MB-atlanta.bin',
			'dallas1.linode.com': 'http://dallas1.linode.com/100MB-dallas.bin',
			'fremont1.linode.com': 'http://fremont1.linode.com/100MB-fremont.bin'}

"""
Ping benchmark
"""
def dc_ping(dcs, ping_time):
	print "==== Ping test ===="
	match_ping_time = "time=[0-9]+" # Match rule for ping time
	match_time = "time=" # Match rule for time from ping time
	dc = 0 # Datacenter number
	best_result = "" # Best datacenter
	best_ping_time = 0 # Best ping time
	
	
	for host,file in dcs.iteritems():
		print "Pinging host: " + host	
	
		# ping and return result
		ping = subprocess.Popen(
			['ping', '-c', ping_time, host],
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE
		)
		out, err = ping.communicate()
	
		# match ping time
		# result: ['time=235', 'time=206', 'time=236', 'time=206', 'time=228', 'time=205', 'time=197', 'time=225', 'time=197', 'time=198']
		regex_ping_time = re.compile(match_ping_time)
		ping_result = regex_ping_time.findall(out)
	
		# get ping time
		# result: Ping fremont1.linode.com 10 times, average response time is: 215 ms
		total_ping_time = 0 # Total ping time number

		for time in ping_result:
			total_ping_time += int(re.sub(match_time, "", time))
		avg_ping_time = total_ping_time / int(ping_time)
	
		# Calcular which datacenter is the best
		if dc == 0: best_ping_time = avg_ping_time
		if avg_ping_time <= best_ping_time:
			best_result = {'time': avg_ping_time, 'host': host}
		if avg_ping_time > 0:
			print "Ping %s %s times, average response time is: %s ms" % (host, ping_time, avg_ping_time)
		else:
			print "%s is died" % (host)
		dc = dc + 1
	
	report = "=== Ping test: best datacenter is %s ===" % (best_result['host'])
	print "=" * len(report)
	print report
	print "=" * len(report)
	
"""
Download benchmark
"""
def dc_down(dcs, download_size):
	print "==== Download test ===="
	dc = 0
	best_time = 0
	for host, file in dcs.iteritems():
		r = urllib2.urlopen(file)
		print "Downloading file %s" % (file)
		start_time = time.time()
		r.read(download_size * 8388608)
		end_time = time.time()
		run_time = end_time - start_time
		print "Download file %s %s MB from %s need %s ms" % (file, download_size, host, run_time)
		if dc == 0: best_time = run_time
		if run_time <= best_time:
			best_result = {'time': best_time, 'host': host}
		dc = dc + 1
	
	report = "=== Download test: best datacenter is %s ===" % (best_result['host'])
	print "=" * len(report)
	print report
	print "=" * len(report)
	
"""
Get parameter from command line
"""
def main(dcs, ping_time, download_size):
	method = 'all'
	time = ping_time
	size = download_size
	# Get value from command line
	parser = argparse.ArgumentParser(description='Benchmark some datacenters.')
	parser.add_argument('-m', '--method', type=str, choices=('all, ping, download'), default=method,
											help='benchmark method, can be ping, download or all')
	parser.add_argument('-t', '--time', type=int, default=time,
											help='ping time default is 10')
	parser.add_argument('-s', '--size', type=float, default=size,
											help='download file size in MB, default is 0.1')
	parser.add_argument('-i', '--ip', type=str, nargs='+',
											help='host name or ip to ping, if you want to download benchmark so -f must be used to indicate which file associate with it')
	parser.add_argument('-f', '--file', type=str, nargs='+',
											help='file location to test download, if you want to ping benchmark, so -i must be used to indicate which host associate with it')
	args = vars(parser.parse_args())

	# Handle customize ip and/or file download
	_dcs = {}
	if args['method'] == 'ping':
		if args['ip']:
			_dcs = dict(zip(args['ip'], range(len(args['ip']))))
	elif args['method'] == 'download':
		if args['file']:
			_dcs = dict(zip(range(len(args['file'])), args['file']))
	elif args['method'] == 'all':
		if args['ip'] and args['file'] and len(args['file']) == len(args['ip']):
			_dcs = dict(zip(args['ip'], args['file']))
	# If user input customize ip / file. Let's use it
	if _dcs : dcs = _dcs
	# Select method to run test
	if args['method'] == 'all' or args['method'] == 'ping' : dc_ping(dcs, str(args['time']))
	if args['method'] == 'all' or args['method'] == 'download' : dc_down(dcs, args['size'])

if __name__ == '__main__':
	main(dcs, ping_time, download_size)
