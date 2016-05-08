#!/usr/bin/env python
from packets import Packets
import os, sys

class Menu:
	def __init__(self):
		self.max_time = 0
		self.packets = Packets()
		self.options = []

	def run(self):
		os.system("clear")
		self.get_packets_csv("udp-15-09-15-2.csv")
		self.get_max_time()
		self.get_options()
		self.packets.sort_packets(self.options)
		self.packets.get_invalid_packets(self.max_time)
		self.packets.get_packet_pair_anaylse(self.packets.invalid_packets)

	def get_packets_csv(self, csv_file):
		'''gets packets from csv file provided as arg
		:param csv_file: file name of csv file that contains packets'''
		try:
			csv_file = open(csv_file, 'r')
			csv_data = [x.replace('"', "") for x in csv_file.readlines()]
			csv_file.close()

			#removes headers from csv data
			csv_data.pop(0)

			#col_indexs = {"num": 0, "time": 1, "src": 2, "dest": 3, "prot": 4, "len": 5, "info": 6}

			for i in csv_data:
				row = i.split(",")
				self.packets.new_packet(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

		except (IOError, NameError, FileNotFoundError):
			raise CSVFileError("Can't access file named: %s" % str(csv_file))
			sys.exit(1)

	def get_max_time(self):
		try:
			self.max_time = float(input("Please enter max time difference as int or float: "))

		except ValueError:
			print("Invalid max time difference entered: {}".format(self.max_time))
			sys.exit(1)

	def get_options(self):
		'''gets user options for packets.'''
		print("Please enter the options for packets below. No spaces.")
		print("Multiple options can be entered by seperating values with a comma")
		print("For example: Protocl: ARP, DHCP, UDP")
		print("Leave option blank for all.")

		options_txt = ["Source IP", "Destination IP", "Protocol", "Length", "Info"]

		#goes through each option get users options
		for i in range(len(options_txt)):
			cur_opt = input("%s: " % options_txt[i])
			#users left option blank for all
			if len(cur_opt) == 0: self.options.append([])
			#strips spaces and splits at ',' to account for any mutliple options
			else: self.options.append(cur_opt.replace(" ", "").split(","))

class CSVFileError(Exception):
	pass

if __name__ == '__main__':
	Menu().run()