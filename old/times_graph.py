#!/usr/bin/env python
import os

def read_csv(f_name):
	try:
		file_ = open(f_name, "r")
		data = file_.readlines()
		file_.close()

	except IOError:
		print "no csv file"
		return -1

	cols = {"packet_num": 0,"time": 1, "prot": 4}
	csv_dict = {}

	for i in range(1, len(data)):
		x = data[i].replace('"', "").split(",")
		numb = x[cols["packet_num"]]
		time = x[cols["time"]]
		prot = x[cols["prot"]]

		if prot != "UDP": continue

		csv_dict[numb] = time
	
	return csv_dict

def main():
	csv_dict = read_csv("udp-15-09-15-2.csv")
	keys = [int(x) for x in csv_dict]
	keys.sort()
	times = []
	last = keys[len(keys) - 1]

	for i in keys:
		time = csv_dict[str(i)]
		times.append(time)

	#for i in keys:
	#	print "%s : %s" % (str(i), csv_dict[str(i)])

if __name__ == '__main__':
	main()