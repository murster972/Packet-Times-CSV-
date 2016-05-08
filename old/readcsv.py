#!/usr/bin/env python
import os

"""
reads csv files
"""

def read_csv(f_name):
	try:
		file_ = open(f_name, "r")
		data = file_.readlines()
		file_.close()

		for i in data: print i

	except IOError:
		print "no csv file"
		return -1

def main():
	read_csv("udp-15-09-15-2.csv")

if __name__ == '__main__':
	main()