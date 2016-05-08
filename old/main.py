#!/usr/bin/env python
import os
import sys
import matplotlib.pyplot as plt

def parse_args():
	"""
	Gets command-line arguments, which is the max time a packet can take to be sent.
	Checks that it's an int or float and that no other arguments have been passed.
	If no arguments have been passed prints an error and exits program
	"""
	try:
		args = [float(sys.argv[x].replace("'", ""))for x in range(1, len(sys.argv))]
	except ValueError:
		print("Please provide and only provide the max time for a packet to be sent as an int/float")
		sys.exit(1)
	if len(args) == 1: return args[0]
	else:
		print("Please provide and only provide the max time for a packet to be sent as an int/float")
		sys.exit(1) 

def get_packets(csv_name):
	"""
	Extracts all packets and their info from 'csv_name'
	:param csv_name: name of csv file containg packet info
	"""
	try:
		csv_file = open(csv_name, 'r')
		csv_data = [x.replace('"', "") for x in csv_file.readlines()]

		cols = {"packet_num": 0, "time": 1, "source": 2, "dest": 3, "prot": 4, "length": 5, "info": 6}

		packets = {}

		for i in range(1, len(csv_data)):
			x = csv_data[i].split(",")
			numb = x[cols["packet_num"]]
			#converts time to float then *1000 for millisecond
			time = float(x[cols["time"]]) * 1000
			source = x[cols["source"]]
			dest = x[cols["dest"]]
			prot = x[cols["prot"]]
			length = x[cols["length"]]
			info = x[cols["info"]]

			packets[int(numb)] = [time, source, dest, prot, length, info]

		return packets

	except IOError:
		print("Cannot find CSV file named %s" % str(csv_name))
		sys.exit(1)

def get_pack_time_diffs(packets):
	"""
	Gets the time differnce between each packets
	returns the time differce between each packet and also the average time diff
	so returns: [[time diff for each packet], average time diff]
	:param packets: dir containg packets, with packet_numb as key and info as array value
	                {packet_num: [packet_info]}
	"""
	keys = [int(x) for x in packets]
	keys.sort()

	packet_time_diffs = []
	time_diffs = []

	#F1 = [0, 1]
	#F2 = [1, 2]
	#Fn is an array consiting of two ints which reprsent the index of an array
	#Fn = [Fn-1[1], fn-1[1] + 1]
	n = [0, 1]

	while n[1] < len(keys):
		curkeys = [keys[n[0]], keys[n[1]]]
		#time in milliseconds
		cur_times = [packets[curkeys[0]][0], packets[curkeys[1]][0]]
		time_diff = cur_times[1] - cur_times[0]
		time_diffs.append(time_diff)
		curkeys.append(time_diff)
		packet_time_diffs.append(curkeys)
		n[0] = n[1]
		n[1] += 1

	average_time_diff = sum(time_diffs) / len(time_diffs)
	#return example: [[], averag time diff]
	return [packet_time_diffs, average_time_diff]

def main():
	os.system("clear")

	"""
	TODO: allow user to pass source ip's, dest ip's, protocols, as command-line args
	"""
	max_pack_time = parse_args() * 1000
	csv_name = "touchtest-gcu.csv"
	packets = get_packets(csv_name)
	UDP_packets = {}

	for x in packets:
		if packets[x][3] == "UDP":
			UDP_packets[x] = packets[x]

	packet_times_diffs = get_pack_time_diffs(UDP_packets)
	average_time_diff = packet_times_diffs[1]
	biggest_time_diff = []
	min_time_diff = []
	tst = 0

	print "The following packets had a time differce between them greater than the average."
	print "They've also been saved in 'problem_packets.txt'"

	problem_file = open("problem_packets1.txt", "w")

	for i in packet_times_diffs[0]:
		if i[2] > max_pack_time:
			packet1 = packets[i[0]]
			packet1.insert(0, i[0])
			packet2 = packets[i[1]]
			packet2.insert(0, i[1])
			time_diff = i[2]
			tst += 1

			problem_file.write(str(packet1) + '\n')
			problem_file.write(str(packet2) + '\n')
			problem_file.write(str(time_diff) + '\n')
			problem_file.write('\n')
	problem_file.close()
	print tst

if __name__ == '__main__':
	main()