#!/usr/bin/env python
from collections import namedtuple, defaultdict

class Packets:
	'''Represents a collection of packets.'''

	def __init__(self):
		self.Packet = namedtuple("Packet", "number, time, source, destination, protocol, length, information")
		self.PacketPair = namedtuple("Packet", "packet_one, packet_two, time_difference")
		self.all_packets = {}
		self.sorted_packets = {}
		self.invalid_packets = []

	def new_packet(self, number, time, src, dest, prot, length, info):
		'''create a new packet and add it to the existing list of packets'''
		self.all_packets[number] = self.Packet(number, time, src, dest, prot, length, info)

	def sort_packets(self, options):
		'''Sorts packets into 'sorted_packets' list, based on the options passed,
		as a tuple in the param, options
		:param options: tuple of packet options'''

		for i in self.all_packets:
			cur_packet = self.all_packets[i]
			matches = []

			for x in range(len(options)):
				cur_opt = options[x]
				cur_packet_opt = cur_packet[x + 2]

				if len(cur_opt) == 0:
					matches.append(1)
					continue

				is_match = [j for j in cur_opt if j == cur_packet_opt]
				if len(is_match) != 0: matches.append(1)

			if len(matches) == 5:
				self.sorted_packets[i] = cur_packet

	def get_time_difference(self, packet1, packet2):
		'''Returns the time difference between two packets'''
		try:
			pack1 = self.sorted_packets[packet1]
			pack2 = self.sorted_packets[packet2]
			time_diff = float(pack2.time) - float(pack1.time)

			return time_diff

		except KeyError:
			print("Packet/s isn't currently in collection of packets.")
			return -1

	def get_invalid_packets(self, max_time):
		'''returns a list of packet pairs whos time difference, is greater
		then max
		:param max_time: max time difference between packets'''
		keys = [x for x in self.sorted_packets]

		n = [0, 1]

		while n[1] < len(self.sorted_packets) + 1:
			try:
				p1 = self.sorted_packets[keys[n[0]]]
				p2 = self.sorted_packets[keys[n[1]]]

			except IndexError:
				p1 = self.sorted_packets[keys[n[0] - 1]]
				p2 = self.sorted_packets[keys[n[1] - 1]]

			time_diff = self.get_time_difference(p1.number, p2.number)

			if time_diff > max_time:
				self.invalid_packets.append(self.PacketPair(p1, p2, time_diff))

			n[0] = n[1]
			n[1] += 1

	def get_packet_pair_anaylse(self, packet_pairs):
		'''prints a similarites of packets between packet pairs
		:param packet_numbers: list of packet pairs'''
		keys = ["Source", "Destination", "Protocol", "Length", "Info"]
		packet_info = [{}, {}, {}, {}, {}]

		for i in packet_pairs:
			current_packets = [self.all_packets[i[0].number], self.all_packets[i[1].number]]
			print("Packets: %s and %s" % (i[0].number, i[1].number))
			print("%d packets between these two packets." % (int(i[1].number) - int(i[0].number) - 1))
			if((int(i[1].number) - int(i[0].number) - 1) > 0):
				packets_between = [self.all_packets[str(x)] for x in range(int(i[0].number) + 1, int(i[1].number))]

				for j in packets_between:
					for x in range(2, len(j)):
						try:
							packet_info[x - 2][j[x]].append(j[0])
						except KeyError:
							packet_info[x - 2][j[x]] = [j[0]]

			if sum([len(x) for x in packet_info]) == 0:
				print("There are no packets between the current packet pair")

			else:
				print("These are the values of the packets between the current pair of packets.")
				for i in range(len(packet_info)):
					values = [x for x in packet_info[i]]
					print("%s had %d different value/s"% (keys[i], len(packet_info[i])))
					print(values)
					print("")
				pause = input()