#!/usr/bin/env python
import os
import sys

#TODO: Make more efficent, and return more info for packets with a greater time diff,
#	   Find better format to output info
#	   output average time, min time and max time between two packets and packets with time diff greater than max
#	   outputn problem packets to txt or csv file

def errors(msg):
	#prints error messages and then exits
	print(msg)
	sys.exit(1)

def parse_args():
	#parses command-line args
	#removes quotion marks from args, and converts to float
	try:
		args = [float(sys.argv[x].replace("'", "")) for x in range(1, len(sys.argv))]
	#returns -1 if value/s passed aren't int or float
	except ValueError:
		errors("Please provide the time gap and only the time gap, as an int or float.")

	#checks that only the time gap has been passed and nothing else, if so returns -1
	if len(args) == 1: return args[0]
	else: errors("Please provide the time gap and only the time gap, as an int or float.")

def get_packets(f_name):
	#gets the time and number of each packet from csv fil and returns as a dict
	try:
		csv_file = open(f_name, "r")
		data = csv_file.readlines()
		csv_file.close()

		#the col of each value
		cols = {"packet_num": 0, "time": 1, "source": 2, "dest": 3, "prot": 4, "length": 5, "info": 6}
		#dict of times: {packet_number: time}
		time_dict = {}

		#loops through each row getting time if a UDP packet
		#starts at 1 as 0 is headings
		for i in range(1, len(data)):
			#removes qoution marks and splits row into list
			x = data[i].replace('"', "").split(",")
			#each index in x is equvilant to a col number
			#for example index 0 = col 0 which is the packet number
			numb = x[cols["packet_num"]]
			time = x[cols["time"]]
			source = x[cols["source"]]
			dest = x[cols["dest"]]
			prot = x[cols["prot"]]
			length = x[cols["length"]]
			info = x[cols["info"]]

			octets_source = source.replace("'", "").split(".")
			try: last_octet_source = int(octets_source[len(octets_source) - 1])
			except ValueError: pass

			#starts new iteration of loop and skips adding to dir if prot if not UDP or source ip last octet is not 11
			if prot != "UDP" or last_octet_source != 11: continue
			time_dict[numb] = [numb, time, source, dest, prot, length, info]
		return time_dict

	except IOError:
		errors("Cannot find CSV file called: %s" % str(f_name))

def find_gaps(time_dir, max_diff):
	#finds time between packets and then returns dir of packets with time difference greater max_diff
	#gets all keys of time_dir and puts them in order so packets can be compared
	keys = [int(x) for x in time_dir]
	keys.sort()

	#list of packets, whos difference is greater than max_diff
	packs = []

	#the index's for list of keys, which are the packet numbers
	n = [0, 1]

	#gets time diff between packets
	while n[1] < len(keys):
		cur_keys = [str(keys[n[0]]), str(keys[n[1]])]
		cur_times = [float(time_dir[cur_keys[0]][1]), float(time_dir[cur_keys[1]][1])]
		diff = cur_times[1] - cur_times[0]
		cur_keys.append(diff)

		if diff >= max_diff:
			packs.append(cur_keys)

		n[0] = n[1]
		n[1] += 1

	return packs

def main():
	os.system("clear")
	time_diff = parse_args()
	csv_name = "udp-15-09-15-2.csv"
	packets = get_packets(csv_name)
	problem_packets = find_gaps(packets, time_diff)

	#opens file that stores packets with time difference > time_diff
	prob_pack_file = open("problem_packets.txt", "w")

	if len(problem_packets) == 0:
		print "No packets with time difference > %f" % time_diff
	else:
		for i in range(len(problem_packets)):
			#writes packets that have a time difference of > tim_diff to txt file in format:
			# packet 1
			# packet 2
			# time difference
			prob_pack1 = packets[problem_packets[i][0]]
			prob_pack2 = packets[problem_packets[i][1]]
			prob_pack_file.write(str(prob_pack1) + '\n')
			prob_pack_file.write(str(prob_pack2) + '\n')
			prob_pack_file.write("Time difference: %f" % float(problem_packets[i][2]) + '\n')
			prob_pack_file.write('\n')

			print str(prob_pack1)
			print str(prob_pack2) + '\n'

		print "The packets above have a time difference > %f , they have also been saved in file called 'problem_packets.txt'" % time_diff
	#closes file
	prob_pack_file.close()

if __name__ == '__main__':
	main()