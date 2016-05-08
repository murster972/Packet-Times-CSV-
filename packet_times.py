#!/usr/bin/env python
import os
import sys

def parse_args():
	"""
	Returns time diff provided by cmd-line arg or -1 if invalid or no time diff provided
	"""
	try:
		time_diff = float(sys.argv[1])
		return time_diff

	except ValueError and IndexError:
		print("Invalid or no time diff provided, average will be used instead.")
		return -1

def get_packets(csv_name):
	"""
	Extracts all packets and their info from 'csv_name'
	:param csv_name: name of csv file containg packet info
	"""
	try:
		csv_file = open(csv_name, 'r')
		csv_data = [x.replace('"', "") for x in csv_file.readlines()]
		csv_file.close()

		#removes headers from csv data
		csv_data.pop(0)

		col_indexs = {"num": 0, "time": 1, "src": 2, "dest": 3, "prot": 4, "len": 5, "info": 6}
		col_names = ["num", "time", "src", "dest", "prot", "len", "info"]
		packets = {}

		for i in csv_data:
			row = i.split(",")
			cur_packet = [row[col_indexs[x]] for x in col_names]
			num = int(row[col_indexs[col_names[0]]])
			packets[num] = cur_packet

		return packets

	except IOError:
		print("Can't access file named: %s" % str(csv_name))
		sys.exit(1)

def sort_packets(opts, packs):
	"""
	returns packets that have options user supplied
	:param opts: options for packets
	:param packs: packets
	"""
	sorted_packets = {}

	for i in packs:
		cur_packet = packs[i]
		matches = []

		for x in range(len(opts)):
			cur_opt = opts[x]
			cur_packet_opt = cur_packet[x + 2]

			if len(cur_opt) == 0:
				matches.append(1)
				continue

			is_match = [j for j in cur_opt if j == cur_packet_opt]
			
			if len(is_match) != 0:
				matches.append(1)

		if len(matches) == 5:
			sorted_packets[i] = cur_packet

	return sorted_packets

def get_packet_time_diff(packets):
	"""
	Gets the time difference between the packets passed
	:param packets: directory of packets
	"""
	#dictionary isn't order so get each key and sort them into order so we can go through
	#packets in order
	packet_numbs = [x for x in packets]
	packet_numbs.sort()

	time_diff = []

	#F1 = (0, 1)
	#F2 = (1, 2)
	#Fn = (I0, I1) #(Index 0, Index 1)
	#Fn = (Fn-1[1], Fn-1[1] + 1)
	n = [0, 1]

	while n[1] < len(packet_numbs) + 1:
		#if odd number of packets last packets time diff is still got
		try:
			packet_1 = packets[packet_numbs[n[0]]]
			packet_2 = packets[packet_numbs[n[1]]]

		except IndexError:
			packet_1 = packets[packet_numbs[n[0] - 1]]
			packet_2 = packets[packet_numbs[n[1] - 1]]

		cur_time_diff = (float(packet_2[1]) - float(packet_1[1]))
		time_diff.append([int(packet_1[0]), int(packet_2[0]), cur_time_diff])
		n[0] = n[1]
		n[1] += 1

	return time_diff

def packet_similarities(problem_packets, all_packets, max_time_diff):
	"""
	Show similarities between packets with greater than max time diff
	and any packets between the packets
	:param current_packets: the two packets and their time difference, [packet1, packet2, time_diff]
	:param all_packets: the dictionary of all packets
	:param max_time_diff: the maxmimu time difference allowed between packets, either the time the user has
						  provied or the average time difference
	"""
	#packet_info= [src, dest, prot, length, info]
	keys = ["Source", "Destination", "Protocol", "Length", "Info"]
	packet_info = [{}, {}, {}, {}, {}]

	print("The following packets had a time difference greater than the average or max difference provided.")

	for i in problem_packets:
		current_packets = [all_packets[i[0]], all_packets[i[1]]]
		print("Packets: %d and %d" % (i[0], i[1]))
		print("%d packets between these two packets." % (i[1] - i[0] - 1))
		if((i[1] - i[0] - 1) > 0):
			packets_between = [all_packets[x] for x in range(i[0] + 1, i[1])]

			for j in packets_between:
				for x in range(2, len(j)):
					try:
						packet_info[x - 2][j[x]].append(j[0])
					except KeyError:
						packet_info[x - 2][j[x]] = [j[0]]

		if sum([len(x) for x in packet_info]) == 0:
			print("There are no packets between the problem packets")

		else:
			print("These are the values of the packets between the current pair of problem packets.")
			for i in range(len(packet_info)):
				values = [x for x in packet_info[i]]
				print("%s had %d different value/s"% (keys[i], len(packet_info[i])))
				print(values)
				print("")
			pause = raw_input()

def main():
	os.system("clear")
	user_time_diff = parse_args()
	print("This script gets the time difference between packets and returns any packets with big differences.")
	print("Please enter the options for the packets to check(ALL SPACES WILL BE STRIPPED).")
	print("For multiple values per option separate with commas.")
	print("Example: Protocol: UDP, SSH, HTTP")

	options = []
	option_txt = ["Source IP", "Destination IP", "Protocol", "Length", "Info"]

	for i in range(len(option_txt)):
		#fix so blanks or tabs or deleted
		opt = raw_input("%s: " % option_txt[i])
		if len(opt) == 0: options.append([])
		else: options.append(opt.replace(" ", "").split(","))

	packets = get_packets("touchtest-gcu.csv")
	sorted_packets = sort_packets(options, packets)
	packet_time_diffs = get_packet_time_diff(sorted_packets)

	if len(packet_time_diffs) == 0:
		print("No packets with options provided.")
		sys.exit(0)

	average_time_diff = sum([x[2] for x in packet_time_diffs]) / len(packet_time_diffs)
	max_time_diff = average_time_diff if user_time_diff == -1 else user_time_diff
	#packets with time diff greater than max
	problem_packets = [x for x in packet_time_diffs if x[2] > max_time_diff]

	packet_similarities(problem_packets, packets, max_time_diff)

	problem_packets_file = open("problem_packets.txt", 'w')

	for i in problem_packets:
		problem_packets_file.write(str(packets[i[0]]) + '\n')
		problem_packets_file.write(str(packets[i[1]]) + '\n')
		problem_packets_file.write('\n')

	problem_packets_file.close()

	print("The problem packets have be saved in the file 'problem_packets.txt'.")

if __name__ == '__main__':
	main()