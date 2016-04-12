## Streaming Videos from a CDN and do traceroute and pings to the CDN
# trace_cdn.py
# Chen Wang, Mar. 3, 2016
# chenw@cmu.edu
import random
import sys
import os
import logging
import shutil
import time
import csv
from datetime import datetime
from qoe_agent import *
from monitor.ping import *
from test_utils import *
from multiprocessing import freeze_support
from monitor.get_hop_info import *
from communication.connect_locator import *

## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
if __name__ == '__main__':
	if sys.platform == 'win32':
		freeze_support()

	if len(sys.argv) > 2:
		cdn_host = sys.argv[1]
	else:
		cdn_host = "cache.cmu-agens.com"
	if len(sys.argv) > 2:
		num_runs = int(sys.argv[2])
	else:
		num_runs = 5

	video_name = 'BBB'

	## Create Trace CSV file
	client_name = getMyName()
	cur_ts = time.strftime("%m%d%H%M")
	client_ID = client_name + "_" + cur_ts

	trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]
	csv_trace_folder = os.getcwd() + "/dataQoE/"

	try:
		os.stat(csv_trace_folder)
	except:
		os.mkdir(csv_trace_folder)

	csv_trace_file = client_ID + ".csv"
	out_csv_trace = open(csv_trace_folder + csv_trace_file, 'wb')
	out_csv_writer = csv.DictWriter(out_csv_trace, fieldnames=trace_fields)
	out_csv_writer.writeheader()

	### Get the server to start streaming
	manager = "manage.cmu-agens.com"

	#  waitRandom(1, 300)
	for i in range(num_runs):
		## Testing rtt based server selection
		locator_info = get_my_locator(manager)
		print "Connected Locator: ", locator_info
		locator = locator_info['ip']
		selected_srv_addr = cdn_host + '/videos/'
		# client_ID, CDN_SQS, uniq_srvs = qoe_agent(selected_srv_addr, video_name, locator)
		qoe_agent(selected_srv_addr, video_name, locator, client_ID, out_csv_writer)

		if os.path.exists(os.getcwd() + "/tmp/"):
			shutil.rmtree(os.getcwd() + "/tmp/")

	## Close tracefile
	out_csv_trace.close()