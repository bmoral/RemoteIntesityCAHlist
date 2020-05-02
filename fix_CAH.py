#!/usr/bin/env python3
""" @author Benjamin Morales Jr
	@description Speed up the process for making Cards Agains Humanity CSV for use in Playingcards.io
		this is not all inclusive, files may require manual editing with Excell, but for well made lists
		of cards it should work just fine to make the list work with it, and to convert a copy paste from 
		their add/remove cards for adding new bulk cards, since it doesn't allow downloading their list"""
import sys
import csv
import random
import getopt

def usage():
	print("To convert list of prompts/responses to csv for Playingcards.io")
	print("Usage: fix_CAH.py -OPTIONS FILE")
	print("-b	Flag Card list is for black prompt cards")
	print("-w	Flag Card list is for white responce cards")
	print("-s N Splite big lists into smaller random lists for smaller\n     decks in game anf conform to limits")
	print("-c	Convert FILE to plain list, helps clean up a file comgin from a flat out copy from the default cards in game")
	print("-h	Display this help message")
	print("")

"""Write data to file CAHoutput.csv if no filename is given,
   @data list of strings to be written
   @filename(opt) file name of the output file
   using file_object open method to write the file, try to avoid using this method"""
def write(data, filename="CAHoutput.txt"):
	file = open(filename, 'w')
	file.writelines(data)
	file.close()

"""Wrtie csv file from data to CAHoutput.csv if no filename is given
   @data list of strings to be written
   @filename(opt) filename of output csv
   using csv writer function, and with statement, prefered way of doing it"""
def write_csv(data, filename="CAHoutput.csv"):
	with open(filename, "w", newline='') as file:
		file = csv.writer(file)
		if filename == "CAH-white.csv":
			file.writerow(["label", "response"])
		else:
			file.writerow(["label", "prompt"])
		for line in data:
			file.writerow(['', line])

"""Process a text file with a list cards to convert to .csv
   to use for CAH in Playingcards.io
   @file list containing the data from file
   @color White cards end with a period '.' as per the official game
   @return data clear of blank spaces and formatted for white cards"""
def process(file, color):
	out = []

	if color == "white":
		for line in file:
			if line == "\n":
				continue
			if line[-2] == "." or line[-2] == '"':
				out.append(line.rstrip())
			else:
				out.append(line.rstrip() + ".")
	else:
		for line in file:
			if line == "\n":
				continue
			else:
				out.append(line.rstrip())

	return out

"""Convert a file containing a straight copy from 
	Playgingcards.io Remote Insensitivity deck
	@file list of strings read in from file
	@color for labeling purposes """
def convert(file, color):
	out = []
	for line in file:
		if line == "1\n" or line == "\n" or line == "Label\n":
			continue
		out.append(line)
	write(out, "CAH-" + color + ".txt")

""" Read in a file in text mode and add to a list of strings(lines)
	@filename name of file to read from
	@return list of strings containing the lines from the file"""
def read(filename):
	try:
		out = []
		with open(filename, "r") as file:
			for line in file:
				out.append(line)
			return out
	except IOError as err:
		print(err)
		sys.exit(1)
	except ValueError as err:
		print(err)
		sys.exit(1)

"""Randomize the list of cards and split into smaller decks,
   @data original properly formatted long deck
   @n split into n decks
   @return list of lists containging n decks"""
def rand_partition(data, n=3):
	random.shuffle(data)
	return [data[i::n] for i in range (n)]

"""Split long deck into smaller decks
   @data original well fomatted long list
   @decks how many decks do you want
   @color black or white cards, for proper naming"""
def split(data, decks, color=2):
	c = {0:"black", 1:"white", 2:"out"}
	header = data[0]
	out = rand_partition(data[1:], decks)
	n = 0
	for i in out:
		write(list(header) + i, "CAH-{}{}.csv".format(c[color], n))
		n = n + 1

def main(argv):
	color = {"BLACK": 0, "WHITE": 1, "NONE": 2}
	outType = ["black", "white", "output"]
	type = color["NONE"]
	
	try:
		opts, args = getopt.getopt(argv[1:], "bws:ch", "")
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

	if len(args) != 1:
		usage()
		sys.exit(2)

	data = read(args[0])

	for opt, value in opts:
		if opt == "-b":
			type = color["BLACK"]
		elif opt == "-w":
			type = color["WHITE"]
		elif opt == "-s":
			try:
				n = int(value)
			except ValueError:
				usage()
				sys.exit(2)
			print("Splitting into {} decks".format(n))
			split(data, n, type)
			print("success")
			quit()
		elif opt == "-c":
			convert(data, outType[type])
			print("success")
			quit()
		elif opt == "-h":
			usage()
			sys.exit()
		else:
			assert False #UnhandledError, should never reach

	write_csv(process(data, outType[type]), "CAH-{}.csv".format(outType[type]))

	print("success!")

if __name__ == "__main__":
	main(sys.argv)