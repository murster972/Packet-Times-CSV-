#!/usr/bin/python
import os
import sys

def parse_args():
	"""
	parses cmd-line args for max time diff, if user hasn't provied or it's invalid the average will
	be used as max time diff instead
	"""
	try:
		#gets the second cmd-line arg(first is script name), converts to float
		#and returns, if errors occur return -1
		if len(sys.argv) > 1: return float(sys.argv[1])
		else: -1

	except ValueError:
		#cmd-line arg isn't an int or float
		print("Invalid max time difference provided, average time difference will be used as max instead.")
		return -1

def get_packets(csv_name):
	try:
		#opens csv file
		csv_file = open(csv_name, 'r')
		#gets data from csv file removing double quotes from each line
		csv_data = [x.replace('"', "") for x in csv_file.readlines()]
		#closes csv file
		csv_file.close()

		#removes headers from csv data
		csv_data.pop(0)

		#each index in the csv data represents a column, the followig is the column name that
		#corrsponds to each index
		col_indexs = {"num": 0, "time": 1, "src": 2, "dest": 3, "prot": 4, "len": 5, "info": 6}	
		col_names = ["num", "time", "src", "dest", "prot", "len", "info"]

		#all packets in key value pair, [packet number: packet]
		packets = {}

		#goes through each line(row) in the csv file
		for i in csv_data:
			#splits row into list
			row = i.split(",")
			#gets each column value of current packet
			cur_packet = [row[col_indexs[x]] for x in col_names]
			#gets packet number to use as key value
			packet_num = int(row[col_indexs[col_names[0]]])
			#adds packet to dictonary of packets
			packets[packet_num] = cur_packet

		return packets

	except IOError:
		#cannot access csv file provided
		print("Cannot access CSV file: %s" % str(csv_name))
		sys.exit(1)

def sort_packets(options, all_packets):
	"""
	gets all packets that match the options the user provided
	:param all_packets: all packets
	:param options: options for packets
	"""
	#sorted packets in key-value pair, [packet number: packet]
	sorted_packets = {}

	for i in all_packets:
		#current packet
		cur_packet = all_packets[i]
		#list keeps track of how many packet values match option values
		matches = []

		#loops through values for current packet checking if they match options
		for x in range(len(options)):
			cur_option = options[x]
			#gets current packet option, x + 2, as first two values[num, time], are skipped
			cur_packet_option = cur_packet[x + 2]

			#if users left optiom blank, means all values for cur option are valid
			if len(cur_option) == 0:
				#appends 1 to 'matches' to singfy match and goes to next inter of loop
				matches.append(1)
				continue

			#loops through values for current option and appends to list if the value matches
			#the current packet value
			is_match = [j for j in cur_option if j == cur_packet_option]

			#appends 1 to match if cur packet value if equal to one of the cur option values
			if len(is_match) != 0: matches.append(1)

		#there are 5 options fo if matches has a length of 5, it means all packet values are valid, so
		#appends current packet to sorted packets
		if len(matches) == 5: sorted_packets[i] = cur_packet

	return sorted_packets

def get_time_diff(packets):
	"""
	Gets the time difference between the packets passed
	:param packets: packets
	"""
	#dictionary isn't order, so we get each key(which is the packet number), store them in a list
	#and sort them so we can go through the packets in order
	packet_nums = [x for x in packets]
	packet_nums.sort()

	#a list of packet pairs and their time difference
	#[packet1, packet1, time difference]
	time_diffs = []
	
	#n represents the current indexes in the packets
	#so n[0] is the index of the first packet in the pair of packets
	#and n[1] is the index of the second packet in the pair of packets
	#n could be defiended as Fn = (Fn-1[1], Fn-1[1] + 1)
	n = [0, 1]

	#loops through packets as pairs
	#+1 at end so that if theres an odd number of packets the last packet is still included
	while n[1] < len(packet_nums) + 1:
		try:
			#gets packets
			packet_1 = packets[packet_numbs[n[0]]]
			packet_2 = packets[packet_numbs[n[1]]]

		#if odd num of packets
		except IndexError:
			#gets packets
			packet_1 = packets[packet_numbs[n[0] - 1]]
			packet_2 = packets[packet_numbs[n[1] - 1]]

		#gets time diff of cur packets
		cur_time_diff = (float(packet_2[1]) - float(packet_1[1]))
		#adds packet pair and packet pair time diff to list of all time_diffs
		time_diffs.append(int(packet_1[0]), int(packet_2[0]), cur_time_diff)
		n[0] = n[1]
		n[1] += 1

	return time_diff

def packet_simil(problem_packets, all_packets):
	pass

def clear():
	"""
	Clears screen, using cmd aprop to OS
	"""
	if os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")

def main():
	clear()
	time_diff = parse_args()
	print("This script gets the time difference between packets and returns any packets with a big time difference.")
	print("Please enter the options for packets below. No spaces.")
	print("Multiple options can be entered by seperating values with a comma")
	print("For example: Protocl: ARP, DHCP, UDP")
	print("Leave option blank for all.")

	#options for packets
	options = []
	#txt for options
	options_txt = ["Source IP", "Destination IP", "Protocol", "Length", "Info"]

	#goes through each option get users options
	for i in range(len(options_txt)):
		cur_opt = raw_input("%s: " % options_txt[i])
		#users left option blank for all
		if len(cur_opt) == 0: options.append([])
		#strips spaces and splits at ',' to account for any mutliple options
		else: options.append(cur_opt.replace(" ", "").split(","))

	csv_name = "touchtest-gcu.csv"
	#gets all packets
	all_packets = get_packets(csv_name)
	#only packets that match options provied
	sorted_packets = sort_packets(options, all_packets)
	#gets time diff between sorted packets
	packet_time_diffs = get_time_diff(sort_packets)

	for x in sorted_packets:
		print(sorted_packets[x])

if __name__ == '__main__':
	main()